import os

from pydantic_settings import BaseSettings



class Settings(BaseSettings):

    
    API_BASE_URL: str | None = os.getenv('API_BASE_URL')
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    
    class Config:
        env_file = ".env"

settings = Settings()