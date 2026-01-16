from app.repository.authRepo import AuthRepository
from app.db.schema.auth import RegisterUser, RegisterOutput, LoginUser, LoginOutput
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.services.emailService import EmailService
from datetime import datetime
from app.core.config import settings

class AuthService:
    def __init__(self, session: Session):
        self.auth_repo = AuthRepository(session=session)

    #-------------------#
    # Register new user #
    #-------------------#
    async def register_user(self, data: RegisterUser) -> RegisterOutput:
        if self.auth_repo.user_exist_by_email(email=data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please login. An account with this email already exists.")
        
        hash_password = HashHelper.get_password_hash(plain_password=data.password)
        data.password = hash_password

        user = self.auth_repo.register_user(user_data=data)

        # Send verification email
        email_service = EmailService()
        await email_service.send_verification_email(email=user.email)

        return user
    
    #------------#
    # Login user #
    #------------#
    async def login_user(self, data: LoginUser) -> LoginOutput:
        if not self.auth_repo.user_exist_by_email(email=data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please create an Account.")
        
        user = self.auth_repo.get_user_by_email(email=data.email)

        if not user.is_verified or user.verified_at is None:
            # Send verification email if not verified
            email_service = EmailService()
            await email_service.send_verification_email(email=user.email)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified. Please verify your email to login.")
        
        if HashHelper.verify_password(plain_password=data.password, hashed_password=user.password):
            user.token_version += 1
            # sign/generate jwt token
            token = AuthHandler.sign_jwt(user_id=user.id, token_version=user.token_version)

            if token:
                return LoginOutput(token_type="Bearer", token=token, expire_in_min=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process request")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please check your credentials.")

    #-------------------#
    # Verify user email #
    #-------------------#
    def verify_email(self, email: str):
        if not email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token payload")
        
        user = self.auth_repo.get_user_by_email(email=email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user.is_verified:
            return {"message": "Email is already verified"}

        user.is_verified = True
        user.verified_at = datetime.utcnow()

        return user
        
    # Get user by id
    def get_user_by_id(self, user_id: int):
        user = self.auth_repo.get_user_by_id(user_id=user_id)

        if user:
            return user
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
