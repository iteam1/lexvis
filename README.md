# LexVis - ANTLR Token Visualizer

LexVis is a web-based tool for visualizing tokens recognized by ANTLR grammars, including whitespace and other channels. It provides an interactive interface to see how your ANTLR grammar processes input text.

## ✨ Features

- **Grammar Upload**: Upload your ANTLR grammar files (.g4)
- **Interactive Tokenization**: Input text and see it tokenized in real-time
- **Token Visualization**: Color-coded tokens with detailed information
- **Raw Data View**: Toggle between visual and raw JSON output
- **Responsive Design**: Works on both desktop and mobile devices
- **Example Grammars**: Comes with sample grammars to get you started

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or later)
- Python 3.8 or later
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iteam1/lexvis.git
   cd lexvis
   ```

2. **Set up the backend**
   ```bash
   # Create and activate a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

1. **Start the backend server** (in the project root)
   ```bash
   source venv/bin/activate  # If not already activated
   uvicorn backend.main:app --reload
   ```

2. **Start the frontend development server** (in a new terminal)
   ```bash
   cd frontend
   npm start
   ```

3. **Open your browser** to `http://localhost:3000`

## 🛠️ Usage

1. **Upload a Grammar**
   - Click "Upload Grammar" and select your `.g4` file
   - Or use one of the example grammars provided

2. **Enter Input Text**
   - Type or paste text you want to tokenize in the input area
   - Use the example text as a starting point

3. **View Results**
   - See color-coded tokens in the visualization panel
   - Toggle between visual and raw JSON views
   - Hover over tokens to see detailed information

## 📁 Project Structure

```
lexvis/
├── backend/           # FastAPI backend
│   └── main.py        # Main API endpoints
├── frontend/          # React frontend
│   ├── public/        # Static files
│   └── src/           # React components and logic
├── examples/          # Example input files
├── grammars/          # Sample ANTLR grammars
└── requirements.txt   # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ANTLR](https://www.antlr.org/) - Powerful parser generator
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Ant Design](https://ant.design/) - Enterprise-class UI design language

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
