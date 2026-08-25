from pydantic_settings import BaseSettings
from pydantic import ConfigDict

# 環境変数の設定
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    
    model_config = ConfigDict(env_file=".env")

settings = Settings()