from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Diia SDK Example"
    app_description: str = "Diia SDK Example"
    app_version: str = "dev"
    debug: bool = False
    # Routes authorization
    basic_auth_username: str = Field(...)
    basic_auth_password: str = Field(...)
    # Basic Diia
    host: str = Field(...)
    acquirer_token: str = Field(...)
    auth_acquirer_token: str = Field(...)
    # User's key data
    key: str = Field(...)
    password: str = Field(...)
    certificate: str = Field(...)
    subject_key_id: str = Field(...)
    # Diia certificates
    diia_certificate: str = Field(...)
    diia_certificate_kep: str = Field(...)
    diia_issuer_certificate: Optional[str] = Field(None)
    model_config = SettingsConfigDict(env_prefix="diia_")


settings = Settings()
