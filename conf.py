from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    secret_key : str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes : int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

settings = Settings()