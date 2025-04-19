from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False

    database_url: str = "sqlite:///sem2.db"

    secret_key: str = "123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    broker_url: str
    images_dir: str
    static_content_path: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
