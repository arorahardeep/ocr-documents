from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
import json
from typing import List, Optional
import aiofiles
from pathlib import Path

from models import DocumentResponse, PageData, ExtractedField
from services.pdf_service import PDFService
from services.ocr_service import OCRService
from config import settings

app = FastAPI(title="OCR Document Processor", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for serving uploaded PDFs
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Initialize services
pdf_service = PDFService()
ocr_service = OCRService()

@app.get("/")
async def root():
    return {"message": "OCR Document Processor API"}

@app.post("/upload-pdf", response_model=DocumentResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    key_fields: str = Form(...)
):
    """
    Upload a PDF file and extract specified fields using OCR
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate file size
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size too large")
        
        # Generate unique document ID
        doc_id = str(uuid.uuid4())
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf")
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Parse key fields
        fields_list = [field.strip() for field in key_fields.split(',') if field.strip()]
        
        # Process PDF
        pages_data = await pdf_service.process_pdf(file_path, fields_list)
        
        # Create response
        response = DocumentResponse(
            doc_id=doc_id,
            filename=file.filename,
            total_pages=len(pages_data),
            key_fields=fields_list,
            pages=pages_data
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: str):
    """
    Get document information and extracted data
    """
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Load cached results if available
        cache_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_results.json")
        if os.path.exists(cache_path):
            async with aiofiles.open(cache_path, 'r') as f:
                content = await f.read()
                return json.loads(content)
        
        raise HTTPException(status_code=404, detail="Document not processed")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document/{doc_id}/page/{page_num}")
async def get_page(doc_id: str, page_num: int):
    """
    Get specific page data
    """
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Load cached results
        cache_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_results.json")
        if not os.path.exists(cache_path):
            raise HTTPException(status_code=404, detail="Document not processed")
        
        async with aiofiles.open(cache_path, 'r') as f:
            content = await f.read()
            doc_data = json.loads(content)
        
        if page_num < 1 or page_num > len(doc_data['pages']):
            raise HTTPException(status_code=404, detail="Page not found")
        
        return doc_data['pages'][page_num - 1]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "OCR Document Processor"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
