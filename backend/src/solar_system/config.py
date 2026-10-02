from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from SOLAR_* enviroment variables."""

    model_config = SettingsConfigDict(env_prefix="SOLAR_")

    data_dir: Path = Path("data")
