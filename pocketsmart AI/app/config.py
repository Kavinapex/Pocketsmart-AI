import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-secret-key"

    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str = ""

    gemini_model: str = "gemini-2.5-flash"

    cors_origins: str = (
        "http://localhost:8501,"
        "http://127.0.0.1:8501"
    )

    @property
    def cors_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


_settings = Settings()


def get_settings() -> Settings:
    return _settings