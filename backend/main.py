from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import antlr4
from antlr4 import *
import os
import tempfile
import importlib.util
import sys
import subprocess
import shutil
from pathlib import Path

app = FastAPI(title="LEXVIS: ANTLR Token Visualizer")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenInfo(BaseModel):
    text: str
    type: str
    line: int
    column: int
    channel: int
    token_index: int
    start: int
    stop: int

class TokenizeResponse(BaseModel):
    tokens: List[TokenInfo]
    input_text: str

def get_token_type_name(lexer, token_type: int) -> str:
    """Convert token type number to its name if possible"""
    if hasattr(lexer, 'symbolicNames') and token_type < len(lexer.symbolicNames):
        name = lexer.symbolicNames[token_type]
        if name != '<INVALID>':
            return name
    return str(token_type)

def generate_lexer_parser(grammar_path: str, output_dir: str) -> None:
    """Generate lexer and parser from ANTLR grammar file."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Path to the ANTLR JAR file in the project's lib directory
    antlr_jar = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'lib', 'antlr-4.13.1-complete.jar')
    
    if not os.path.exists(antlr_jar):
        raise FileNotFoundError(f"ANTLR JAR not found at {antlr_jar}")
    
    # Run ANTLR tool to generate lexer and parser
    cmd = ["java", "-jar", antlr_jar,
           "-Dlanguage=Python3", 
           "-o", output_dir, 
           "-visitor",  # Generate parse tree visitor
           "-no-listener",  # Don't generate parse tree listener
           grammar_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"ANTLR generation output: {result.stdout}")
        if result.stderr:
            print(f"ANTLR generation warnings: {result.stderr}")
    except subprocess.CalledProcessError as e:
        error_msg = f"Error generating lexer/parser: {e.stderr}"
        print(error_msg)
        raise RuntimeError(error_msg) from e

def load_lexer_module(grammar_name: str, output_dir: str):
    """Dynamically load the generated lexer module."""
    if output_dir not in sys.path:
        sys.path.insert(0, output_dir)
    
    module_name = f"{grammar_name}Lexer"
    module_file = os.path.join(output_dir, f"{module_name}.py")
    
    # Import the module
    spec = importlib.util.spec_from_file_location(module_name, module_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import {module_name} from {module_file}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    # Get the lexer class
    lexer_class = getattr(module, module_name, None)
    if lexer_class is None:
        raise ImportError(f"Could not find {module_name} class in {module_file}")
    
    return lexer_class

@app.post("/api/tokenize", response_model=TokenizeResponse)
async def tokenize_grammar(grammar_file: UploadFile = File(...), input_text: str = ""):
    """
    Tokenize input text using the provided ANTLR grammar file.
    """
    temp_dir = tempfile.mkdtemp()
    grammar_path = os.path.join(temp_dir, grammar_file.filename)
    
    try:
        # Save the uploaded grammar file
        with open(grammar_path, 'wb') as f:
            content = await grammar_file.read()
            f.write(content)
        
        # Extract grammar name from the grammar file
        with open(grammar_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('grammar'):
                grammar_name = first_line.split()[1].rstrip(';')
            else:
                grammar_name = Path(grammar_file.filename).stem
        
        # Generate lexer and parser
        generate_lexer_parser(grammar_path, temp_dir)
        
        # Load the generated lexer
        Lexer = load_lexer_module(grammar_name, temp_dir)
        
        # Create input stream and tokenize
        input_stream = InputStream(input_text)
        lexer = Lexer(input_stream)
        
        # Get all tokens
        tokens = []
        token = lexer.nextToken()
        
        while token.type != Token.EOF:
            token_type = lexer.symbolicNames[token.type] if token.type < len(lexer.symbolicNames) else str(token.type)
            
            tokens.append({
                'text': token.text,
                'type': token_type,
                'line': token.line,
                'column': token.column,
                'channel': token.channel,
                'token_index': token.tokenIndex,
                'start': token.start,
                'stop': token.stop,
                'type_id': token.type
            })
            
            token = lexer.nextToken()
        
        return {
            'tokens': tokens,
            'input_text': input_text,
            'grammar': grammar_name
        }
        
    except Exception as e:
        error_msg = f"Error processing grammar: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error_msg)
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.get("/")
async def read_root():
    return {"message": "ANTLR Token Visualizer API is running"}
