from fastapi_mail import FastMail, MessageSchema
from app.utils.email_config import conf
from app.core.security.authHandler import AuthHandler
from app.core.config import settings
import os

class EmailService:
    @staticmethod
    async def send_verification_email(email: str):
        token = AuthHandler.generate_email_token(email=email)
        verify_link = f"{settings.FRONTEND_URL}/v1/auth/verify-email?token={token}"

        message = MessageSchema(
            subject="Email Verification",
            recipients=[email],
            body=f"""
            <h3>Please click the link below to verify your email address:</h3>
            <a href="{verify_link}">Verify Email</a>
            """,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    def verify_email_token(token: str) -> dict:
        return AuthHandler.verify_email_token(token=token)