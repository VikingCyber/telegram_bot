from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class Settings(BaseSettings):
    bot_token: SecretStr
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
