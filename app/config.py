from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mistral_api_key: str
    mistral_model: str = "mistral-small-latest"  # free tier: 1M tokens/month
    internal_api_secret: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
