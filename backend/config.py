import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    
    # OCR Configuration
    SUPPORTED_LANGUAGES: List[str] = [
        "en", "th", "zh", "id", "vi", "ja", "ko", "es", "fr", "de", "it", "pt", "ru", "ar"
    ]
    
    # Model Configuration
    DEFAULT_MODEL: str = "gpt-5-nano"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 1

settings = Settings()
