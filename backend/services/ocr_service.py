import time
import json
from typing import List, Dict, Any
import openai
from openai import OpenAI

from models import ExtractedField
from config import settings

class OCRService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
    
    async def extract_fields(self, image_base64: str, key_fields: List[str], page_number: int) -> List[ExtractedField]:
        """
        Extract specified fields from an image using OpenAI's GPT-4 Vision
        """
        start_time = time.time()
        
        try:
            # Create the prompt for field extraction
            prompt = self._create_extraction_prompt(key_fields)
            
            # Prepare the message for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert OCR system that extracts specific fields from documents. Return only valid JSON with the extracted fields."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_completion_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            content = response.choices[0].message.content
            extracted_data = json.loads(content)
            
            # Convert to ExtractedField objects
            extracted_fields = []
            for field_name, field_data in extracted_data.items():
                if isinstance(field_data, dict):
                    value = field_data.get('value', '')
                    confidence = field_data.get('confidence', 0.8)
                else:
                    value = str(field_data)
                    confidence = 0.8
                
                extracted_field = ExtractedField(
                    field_name=field_name,
                    value=value,
                    confidence=confidence,
                    page_number=page_number
                )
                extracted_fields.append(extracted_field)
            
            processing_time = time.time() - start_time
            
            return extracted_fields
            
        except Exception as e:
            # Return empty fields if extraction fails
            print(f"Error in OCR extraction: {str(e)}")
            return []
    
    def _create_extraction_prompt(self, key_fields: List[str]) -> str:
        """
        Create a detailed prompt for field extraction
        """
        fields_text = ", ".join([f'"{field}"' for field in key_fields])
        
        prompt = f"""
        Analyze this document image and extract the following fields: {fields_text}

        Instructions:
        1. Look for the specified fields in the document
        2. For each field, provide the extracted value and confidence level (0.0 to 1.0)
        3. If a field is not found, set its value to empty string and confidence to 0.0
        4. Handle multiple languages (English, Thai, Mandarin, Bahasa, Vietnamese, etc.)
        5. For dates, use ISO format (YYYY-MM-DD) when possible
        6. For amounts/numbers, extract the numerical value
        7. For names, extract the full name as it appears

        Return the results in this exact JSON format:
        {{
            "field_name": {{
                "value": "extracted_value",
                "confidence": 0.95
            }}
        }}

        Example response:
        {{
            "invoice_number": {{
                "value": "INV-2024-001",
                "confidence": 0.98
            }},
            "date": {{
                "value": "2024-01-15",
                "confidence": 0.95
            }},
            "amount": {{
                "value": "1,250.00",
                "confidence": 0.92
            }}
        }}

        Be precise and accurate in your extraction. If you're unsure about a field, set confidence lower.
        """
        
        return prompt
    
    async def detect_language(self, image_base64: str) -> str:
        """
        Detect the primary language in the document
        """
        try:
            prompt = """
            Analyze this document image and identify the primary language used.
            Return only the language code (e.g., 'en', 'th', 'zh', 'id', 'vi').
            If multiple languages are present, return the most dominant one.
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a language detection expert. Return only the language code."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=10,
                temperature=0.1
            )
            
            language = response.choices[0].message.content.strip().lower()
            
            # Map common language names to codes
            language_map = {
                'english': 'en',
                'thai': 'th',
                'mandarin': 'zh',
                'chinese': 'zh',
                'indonesian': 'id',
                'bahasa': 'id',
                'vietnamese': 'vi',
                'japanese': 'ja',
                'korean': 'ko',
                'spanish': 'es',
                'french': 'fr',
                'german': 'de',
                'italian': 'it',
                'portuguese': 'pt',
                'russian': 'ru',
                'arabic': 'ar'
            }
            
            return language_map.get(language, language)
            
        except Exception as e:
            print(f"Error in language detection: {str(e)}")
            return 'en'  # Default to English
    
    def validate_extraction(self, extracted_fields: List[ExtractedField]) -> List[ExtractedField]:
        """
        Validate and clean extracted fields
        """
        validated_fields = []
        
        for field in extracted_fields:
            # Clean the value
            cleaned_value = field.value.strip() if field.value else ""
            
            # Adjust confidence based on value quality
            confidence = field.confidence
            if not cleaned_value:
                confidence = 0.0
            elif len(cleaned_value) < 2:
                confidence = min(confidence, 0.5)
            
            validated_field = ExtractedField(
                field_name=field.field_name,
                value=cleaned_value,
                confidence=confidence,
                page_number=field.page_number
            )
            validated_fields.append(validated_field)
        
        return validated_fields
