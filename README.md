# OCR Document Processor

A web-based OCR application that extracts key fields from PDF documents using OpenAI's GPT-5 model. Supports multiple languages and multi-page documents.

## Features

- 📄 PDF upload and preview (scanned or digital)
- 🌍 Multi-language support (Thai, Mandarin, Bahasa, Vietnamese, English)
- 📊 Custom field extraction with JSON output
- 📱 Responsive web interface
- 🔄 Multi-page document navigation
- 🎨 Modern UI with Tailwind CSS

## Tech Stack

### Frontend
- React 18
- Node.js
- Tailwind CSS
- Axios for API calls

### Backend
- Python 3.9+
- FastAPI
- OpenAI GPT-5 (latest vision model)
- PyMuPDF for PDF processing
- Pillow for image processing

## Project Structure

```
ocr-documents/
├── frontend/          # React frontend application
├── backend/           # Python FastAPI backend
├── README.md         # This file
└── .env.example      # Environment variables template
```

## Setup Instructions

### Prerequisites
- Node.js 16+
- Python 3.9+
- OpenAI API key

### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. Run the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Upload a PDF document (scanned or digital)
3. Enter the key fields you want to extract (comma-separated)
4. Click "Process Document" to start OCR extraction
5. Navigate through pages using the pagination controls
6. View extracted fields in the table on the right side

## API Endpoints

- `POST /upload-pdf` - Upload and process PDF
- `GET /document/{doc_id}` - Get document details
- `GET /document/{doc_id}/page/{page_num}` - Get specific page data

## Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=uploads
```

## License

MIT License
