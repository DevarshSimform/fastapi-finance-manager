from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the application, loaded from environment variables or a .env file."""

    DATABASE_URL: str

    EMAIL_SECRET_KEY: str
    GENERAL_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    REDIS_BROKER_URL: str
    TEMPLATE_PATH: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    BASE_URL: str = "http://localhost:8000"

    SESSION_SECRET_KEY: str

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
