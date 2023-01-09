import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int = 60 * 24 * 10  # 10 days
    ACCESS_TOKEN_EXPIRES_IN: int = 60  # 60 minutes
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = 'media'
MEDIA_PATH = "{}/{}".format(BASE_DIR, MEDIA_ROOT)
