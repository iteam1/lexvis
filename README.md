# LexVis

A tool for visualizing tokens recognized by ANTLR grammars, including whitespace and other channels.

## Features

- Upload ANTLR grammar files (.g4)
- Input text to tokenize
- Visualize tokens with syntax highlighting
- View raw token data
- Responsive design that works on desktop and mobile

## Prerequisites

- Node.js (v14 or later)
- Python 3.7 or later
- pip (Python package manager)

## Getting Started

### Backend Setup

1. Navigate to the project directory:
   ```bash
   cd antlr-token-visualizer
   ```

2. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. In a new terminal, navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the required Node.js packages:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

## Usage

1. Upload an ANTLR grammar file (.g4)
2. Enter some text to tokenize in the input area
3. Click the "Tokenize" button
4. View the tokenized output in the "Visual" or "Raw Data" tabs

## Project Structure

```
antlr-token-visualizer/
├── backend/               # FastAPI backend
│   └── main.py            # Main backend application
├── frontend/              # React frontend
│   ├── public/            # Static files
│   └── src/               # React source code
│       └── App.tsx        # Main React component
├── grammars/              # Directory for storing grammar files
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
