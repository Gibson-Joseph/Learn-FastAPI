from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    REDIS_URL: str = "redis://localhost:6379/0"

    # Mail Service
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_SSL_TLS: bool = False
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_STARTTLS: bool = True
    MAIL_FROM_NAME: str
    VALIDATE_CERTS: bool = True
    USE_CREDENTIALS: bool = True

    DOMAIN: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()

# Celery config variable
broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True
