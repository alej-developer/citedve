from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RADAR_", env_file=".env", env_file_encoding="utf-8")

    cors_origins: list[str] = ["*"]
    data_dir: str = "../../data"  # Default relative to apps/api when running locally


settings = Settings()
