import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Info
    APP_TITLE: str = "Obesity Level Prediction API"
    APP_VERSION: str = "1.0.0"
    
    # API Key for authentication
    API_KEY: str = ""
    
    # Model paths
    MODEL_DIR: str = os.getenv("MODEL_DIR", "./models")
    
    @property
    def MODEL_PATH(self) -> str:
        return os.path.join(self.MODEL_DIR, "xgb_obesity_model.json")
    
    @property
    def MODEL_PKL_PATH(self) -> str:
        return os.path.join(self.MODEL_DIR, "xgb_obesity_model.pkl")
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()
