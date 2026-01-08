from app.db.models.user import User
from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    # Database configuration settings
    DATABASE_URL: str

    # Email configuration settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool

    # App settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    FRONTEND_URL: str
    EMAIL_TOKEN_EXP_MIN: int

    # RBAC Seed Data
    SEED_ADMIN_EMAIL: EmailStr
    SEED_ADMIN_PASSWORD: str
    SEED_ADMIN_FIRST_NAME: str
    SEED_ADMIN_LAST_NAME: str

    SEED_USER_EMAIL: EmailStr
    SEED_USER_PASSWORD: str
    SEED_USER_FIRST_NAME: str
    SEED_USER_LAST_NAME: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()