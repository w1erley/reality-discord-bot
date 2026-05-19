from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    token: str = Field(alias="TOKEN")
    prefix: str = Field(default="!", alias="PREFIX")
    invite_link: str = Field(default="", alias="INVITE_LINK")
    db_path: str = Field(default="data/database.db", alias="DB_PATH")


@lru_cache
def get_settings() -> Settings:
    return Settings()
