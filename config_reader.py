import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class Settings(BaseSettings):
    bot_token: SecretStr
    BASE_DIR: Path = os.path.dirname(os.path.abspath(__file__))
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
