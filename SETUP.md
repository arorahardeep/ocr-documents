# OCR Document Processor - Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys) (requires GPT-5 access)

### Automatic Setup (Recommended)

#### macOS/Linux
```bash
# Make the startup script executable
chmod +x start.sh

# Run the startup script
./start.sh
```

#### Windows
```cmd
# Run the startup script
start.bat
```

### Manual Setup

#### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=uploads

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### API Endpoints

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Features

### ✅ Implemented Features
- [x] PDF upload and preview (scanned and digital)
- [x] Multi-language OCR support (Thai, Mandarin, Bahasa, Vietnamese, English, etc.)
- [x] Custom field extraction with user-defined fields
- [x] Multi-page document support with page navigation
- [x] Real-time field extraction using OpenAI GPT-4 Vision
- [x] Confidence scoring for extracted fields
- [x] Modern responsive UI with Tailwind CSS
- [x] JSON export functionality
- [x] Copy-to-clipboard for individual fields
- [x] PDF zoom, rotate, and navigation controls
- [x] Error handling and validation
- [x] Loading states and progress indicators

### 🎯 Key Capabilities
- **Multi-language Support**: Automatically detects and processes documents in multiple languages
- **Flexible Field Extraction**: Users can specify any fields they want to extract
- **High Accuracy**: Uses OpenAI's GPT-5 model for superior OCR accuracy
- **User-Friendly Interface**: Intuitive drag-and-drop upload and clean results display
- **Page-by-Page Processing**: Handles multi-page documents with individual page extraction

## 🧪 Testing Your Setup

Run the test script to verify everything is working:

```bash
python test_setup.py
```

## 📁 Project Structure

```
ocr-documents/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main application file
│   ├── config.py           # Configuration settings
│   ├── models.py           # Pydantic models
│   ├── services/           # Business logic services
│   │   ├── pdf_service.py  # PDF processing service
│   │   └── ocr_service.py  # OCR extraction service
│   ├── requirements.txt    # Python dependencies
│   └── env.example        # Environment variables template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js         # Main application component
│   │   └── index.js       # Application entry point
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS configuration
├── start.sh               # macOS/Linux startup script
├── start.bat              # Windows startup script
├── test_setup.py          # Setup verification script
└── README.md              # Main documentation
```

## 🔍 Usage

1. **Upload Document**: Drag and drop or browse for a PDF file
2. **Specify Fields**: Enter the fields you want to extract (comma-separated)
3. **Process**: Click "Process Document" to start OCR extraction
4. **View Results**: Navigate through pages and view extracted fields
5. **Export**: Copy individual fields or export all data as JSON

## 🛠️ Troubleshooting

### Common Issues

#### Backend Issues
- **Module not found errors**: Make sure you're in the virtual environment and have installed requirements
- **OpenAI API errors**: Verify your API key is correct and has sufficient credits
- **Port already in use**: Change the port in the .env file or kill the process using the port

#### Frontend Issues
- **Node modules not found**: Run `npm install` in the frontend directory
- **Port 3000 in use**: React will automatically suggest an alternative port
- **CORS errors**: Make sure the backend is running on the correct port

#### File Upload Issues
- **File too large**: Increase MAX_FILE_SIZE in the .env file
- **Invalid file type**: Only PDF files are supported
- **Upload fails**: Check network connection and backend server status

### Getting Help

1. Run `python test_setup.py` to diagnose setup issues
2. Check the browser console for frontend errors
3. Check the backend logs for API errors
4. Verify your OpenAI API key is valid and has credits

## 🔒 Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The application stores uploaded files temporarily in the `uploads` directory
- Consider implementing authentication for production use
- Monitor API usage to control costs

## 🚀 Deployment

For production deployment:

1. **Backend**: Deploy to a cloud service (AWS, Google Cloud, Azure, etc.)
2. **Frontend**: Build with `npm run build` and serve static files
3. **Environment**: Set up proper environment variables
4. **Security**: Implement authentication and HTTPS
5. **Storage**: Use cloud storage for uploaded files
6. **Monitoring**: Set up logging and monitoring

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Happy Document Processing! 📄✨**
