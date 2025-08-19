# Agentic Document Extraction

A powerful document processing pipeline that extracts structured information from various document types using OCR and AI.

## Features

- **Multi-format Support**: Process PDFs, images, and scanned documents
- **Document Classification**: Automatically detect document types (invoices, receipts, contracts, IDs)
- **Structured Data Extraction**: Extract relevant fields using AI-powered extraction
- **Validation & Confidence Scoring**: Validate extracted data and provide confidence scores
- **Visualization**: Visualize extracted information with bounding boxes
- **REST API**: Easy integration with other services

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agentic-doc-extraction.git
   cd agentic-doc-extraction
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR (required for text extraction):
   - **Windows**: Download and install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

## Usage

### Command Line

```bash
python -m app --input path/to/document.pdf --output results.json
```

### Python API

```python
from agents.ocr_agent import OCRAgent
from agents.extractor import DocumentExtractor

# Initialize agents
ocr_agent = OCRAgent()
extractor = DocumentExtractor(api_key="your_openai_api_key")

# Process a document
result = ocr_agent.process_document("path/to/document.pdf")
extracted_data = extractor.extract(
    text=result["text"],
    schema={"field1": "type1", "field2": "type2"},
    document_type="invoice"
)
```

### Web Interface

Start the web interface:
```bash
uvicorn app:app --reload
```

Then open `http://localhost:8000` in your browser.

## Project Structure

```
agentic-doc-extraction/
├── app.py               # Main application entry point
├── agents/              # Document processing agents
│   ├── __init__.py
│   ├── router.py        # Document type classifier
│   ├── ocr_agent.py     # OCR processing
│   ├── extractor.py     # AI-based extraction
│   ├── validator.py     # Data validation
│   └── confidence.py    # Confidence scoring
├── schemas/             # Data models and schemas
│   ├── __init__.py
│   └── output_schema.py # Pydantic models
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── pdf_utils.py     # PDF processing
│   └── visualize.py     # Visualization tools
├── data/                # Sample documents
├── outputs/             # Extracted data
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Configuration

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TESSERACT_CMD=/usr/bin/tesseract  # Path to Tesseract executable
```

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
