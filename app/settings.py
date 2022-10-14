from pathlib import Path
from pydantic import BaseSettings, PostgresDsn, Field, PositiveInt

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")

    host: str = Field("0.0.0.0", env="HOST")
    port: PositiveInt = Field(80, env="PORT")

    db_url: PostgresDsn = Field(..., env="DATABASE_URL")


settings = Settings()
