from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import antlr4
from antlr4 import *
import os
import tempfile

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

@app.post("/api/tokenize", response_model=TokenizeResponse)
async def tokenize_grammar(grammar_file: UploadFile = File(...), input_text: str = ""):
    """
    Tokenize input text using the provided ANTLR grammar file.
    """
    try:
        # Save the uploaded grammar file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.g4') as temp_grammar:
            content = await grammar_file.read()
            temp_grammar.write(content)
            grammar_path = temp_grammar.name
        
        # Generate lexer and parser
        # Note: In a production environment, you'd want to compile the grammar
        # and import the generated lexer/parser
        
        # For now, we'll just return a simple tokenization
        # In a real implementation, you would:
        # 1. Generate lexer/parser from the grammar
        # 2. Use them to tokenize the input text
        # 3. Return the tokens with detailed information
        
        # This is a placeholder implementation
        tokens = []
        lexer = antlr4.Lexer(antlr4.InputStream(input_text))
        
        # In a real implementation, you would use the generated lexer
        # from the uploaded grammar file
        
        # For now, just split on whitespace as a simple example
        words = input_text.split()
        for i, word in enumerate(words):
            tokens.append({
                'text': word,
                'type': 'WORD',
                'line': 1,
                'column': 0,  # This would be calculated in a real implementation
                'channel': 0,
                'token_index': i,
                'start': 0,  # These would be calculated in a real implementation
                'stop': len(word) - 1
            })
        
        # Clean up
        os.unlink(grammar_path)
        
        return {
            'tokens': tokens,
            'input_text': input_text
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "ANTLR Token Visualizer API is running"}
