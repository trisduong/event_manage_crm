import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_region: str = "us-east-1"
    dynamodb_host: str = os.getenv("DYNAMODB_HOST", "http://localhost:4566")
    ses_host: str = os.getenv("SES_HOST", "http://localhost:4566")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")


settings = Settings()
