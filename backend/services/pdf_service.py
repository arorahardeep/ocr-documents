import os
import asyncio
import json
from typing import List, Optional
import aiofiles
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import base64

from models import PageData, ExtractedField
from services.ocr_service import OCRService
from config import settings

class PDFService:
    def __init__(self):
        self.ocr_service = OCRService()
    
    async def prepare_pages(self, file_path: str) -> List[PageData]:
        """
        Prepare per-page placeholders without extraction.
        """
        try:
            pdf_document = fitz.open(file_path)
            pages_data: List[PageData] = []
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                # Convert to image preview
                mat = fitz.Matrix(2.0, 2.0)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                # No actual file save here; preview via /uploads/pdf path
                page_data = PageData(
                    page_number=page_num + 1,
                    extracted_fields=[],
                    page_image_url=f"/uploads/{Path(file_path).stem}.pdf#page={page_num + 1}",
                    text_content=None,
                    processing_time=None
                )
                pages_data.append(page_data)
            pdf_document.close()
            # Save empty results cache
            await self._save_results(file_path, pages_data, key_fields=[])
            return pages_data
        except Exception as e:
            raise Exception(f"Error preparing pages: {str(e)}")

    async def process_page(self, file_path: str, page_num: int, key_fields: List[str]) -> PageData:
        """
        Process a single page and extract specified fields.
        """
        try:
            pdf_document = fitz.open(file_path)
            if page_num < 1 or page_num > len(pdf_document):
                raise ValueError("Invalid page number")
            page = pdf_document[page_num - 1]

            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            extracted_fields = await self.ocr_service.extract_fields(
                img_base64, key_fields, page_num
            )

            page_data = PageData(
                page_number=page_num,
                extracted_fields=extracted_fields,
                page_image_url=f"/uploads/{Path(file_path).stem}.pdf#page={page_num}",
                text_content=page.get_text(),
                processing_time=None
            )
            pdf_document.close()
            return page_data
        except Exception as e:
            raise Exception(f"Error processing page: {str(e)}")

    async def process_pdf(self, file_path: str, key_fields: List[str]) -> List[PageData]:
        """
        Process a PDF file and extract specified fields from each page
        """
        try:
            # Open PDF
            pdf_document = fitz.open(file_path)
            pages_data = []
            
            # Process each page
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2.0, 2.0)  # Scale factor for better quality
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                
                # Convert to base64 for API
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                
                # Extract text using OCR
                extracted_fields = await self.ocr_service.extract_fields(
                    img_base64, key_fields, page_num + 1
                )
                
                # Create page data
                page_data = PageData(
                    page_number=page_num + 1,
                    extracted_fields=extracted_fields,
                    page_image_url=f"/uploads/{Path(file_path).stem}_page_{page_num + 1}.png",
                    text_content=page.get_text(),
                    processing_time=None  # Will be set by OCR service
                )
                
                pages_data.append(page_data)
            
            pdf_document.close()
            
            # Save results to cache
            await self._save_results(file_path, pages_data, key_fields)
            
            return pages_data
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    async def _save_results(self, file_path: str, pages_data: List[PageData], key_fields: List[str]):
        """
        Save processing results to cache file
        """
        try:
            doc_id = Path(file_path).stem
            cache_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_results.json")
            
            # Convert to dict for JSON serialization
            results = {
                "doc_id": doc_id,
                "filename": Path(file_path).name,
                "total_pages": len(pages_data),
                "key_fields": key_fields,
                "pages": [page.dict() for page in pages_data],
                "processing_status": "completed",
                "created_at": str(__import__("datetime").datetime.now())
            }
            
            async with aiofiles.open(cache_path, 'w') as f:
                await f.write(json.dumps(results, indent=2, default=str))
                
        except Exception as e:
            print(f"Warning: Could not save results cache: {str(e)}")
    
    def get_page_count(self, file_path: str) -> int:
        """
        Get the number of pages in a PDF file
        """
        try:
            pdf_document = fitz.open(file_path)
            page_count = len(pdf_document)
            pdf_document.close()
            return page_count
        except Exception as e:
            raise Exception(f"Error getting page count: {str(e)}")
    
    def extract_text_from_page(self, file_path: str, page_num: int) -> str:
        """
        Extract text from a specific page
        """
        try:
            pdf_document = fitz.open(file_path)
            if page_num < 0 or page_num >= len(pdf_document):
                raise ValueError("Invalid page number")
            
            page = pdf_document[page_num]
            text = page.get_text()
            pdf_document.close()
            return text
            
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    def convert_page_to_image(self, file_path: str, page_num: int, output_path: str, scale: float = 2.0):
        """
        Convert a specific page to image and save it
        """
        try:
            pdf_document = fitz.open(file_path)
            if page_num < 0 or page_num >= len(pdf_document):
                raise ValueError("Invalid page number")
            
            page = pdf_document[page_num]
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat)
            
            # Save image
            pix.save(output_path)
            pdf_document.close()
            
        except Exception as e:
            raise Exception(f"Error converting page to image: {str(e)}")
