import os
from pathlib import Path

from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = Field(default="dev", alias="ENVIRONMENT")
    oauth_client_id: str = Field("error", alias="GOOGLE_OAUTH_CLIENT_ID")
    oauth_client_secret: str = Field("error", alias="GOOGLE_OAUTH_CLIENT_SECRET")
    port: int = Field(8001, alias="PORT")
    allowed_origins: str = Field("http://localhost", alias="ALLOWED_ORIGINS")
    data_dir: str = Field(os.getcwd() + "/data", alias="DATA_DIR")

    @property
    def allowed_origins_list(self) -> list[str]:
        return self.allowed_origins.split(",")

    @property
    def data_dir_path(self) -> Path:
        return Path(self.data_dir)


Config = Settings()  # type: ignore
