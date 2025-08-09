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

from models import DocumentResponse, PageData, ExtractedField, PageExtractRequest
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
    file: UploadFile = File(...)
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
        
        # No upfront fields; create empty per-page data placeholders
        pages_data = await pdf_service.prepare_pages(file_path)
        
        # Create response
        response = DocumentResponse(
            doc_id=doc_id,
            filename=file.filename,
            total_pages=len(pages_data),
            key_fields=[],
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

@app.post("/document/{doc_id}/page/{page_num}/extract")
async def extract_fields_for_page(doc_id: str, page_num: int, req: PageExtractRequest):
    """
    Extract specified fields for a single page.
    """
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document not found")

        page_data = await pdf_service.process_page(file_path, page_num, req.key_fields)

        # Update cache file minimally
        cache_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_results.json")
        if os.path.exists(cache_path):
            async with aiofiles.open(cache_path, 'r') as f:
                content = await f.read()
                doc_data = json.loads(content)
        else:
            doc_data = {"doc_id": doc_id, "filename": Path(file_path).name, "total_pages": page_data.page_number, "key_fields": [], "pages": []}

        # Ensure pages array length
        while len(doc_data.get("pages", [])) < page_num:
            doc_data.setdefault("pages", []).append({"page_number": len(doc_data["pages"]) + 1, "extracted_fields": [], "page_image_url": None, "text_content": None, "processing_time": None})

        doc_data["pages"][page_num - 1] = page_data.dict()

        async with aiofiles.open(cache_path, 'w') as f:
            await f.write(json.dumps(doc_data, indent=2, default=str))

        return page_data
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
