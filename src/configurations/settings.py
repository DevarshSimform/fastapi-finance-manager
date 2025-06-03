from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    REDIS_BROKER_URL: str
    TEMPLATE_PATH: str

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
