from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")

    name: str
    user: str
    host: str
    port: int
    password: str


class CsrfSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CSRF_", env_file=".env", extra="ignore"
    )

    trusted_origins: list[str]


class DjangoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DJANGO_", env_file=".env", extra="ignore"
    )

    debug: bool = Field(default=False)
    allowed_hosts: list[str]
    secret_key: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    db: DbSettings = Field(default_factory=DbSettings)
    csrf: CsrfSettings = Field(default_factory=CsrfSettings)
    django: DjangoSettings = Field(default_factory=DjangoSettings)
