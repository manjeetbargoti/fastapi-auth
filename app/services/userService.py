from app.repository.userRepo import UserRepository
from app.db.schema.user import UserInCreate, UserOutput, UserInLogin, UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.services.emailService import EmailService
from datetime import datetime
from app.core.config import settings

class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session=session)
    
    # User registration
    async def signup(self, data: UserInCreate) -> UserOutput:
        if self.repo.user_exist_by_email(email=data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please login. An account with this email already exists.")
        
        hashed_password = HashHelper.get_password_hash(plain_password=data.password)
        data.password = hashed_password

        user  = self.repo.create_user(data)
        
        # Send verification email
        email_service = EmailService()
        await email_service.send_verification_email(email=user.email)

        return user

    # User login route
    async def login(self, data: UserInLogin) -> UserWithToken:
        if not self.repo.user_exist_by_email(email=data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please create an Account.")
        
        user = self.repo.get_user_by_email(email=data.email)
        if not user.is_verified:
            # Send verification email
            email_service = EmailService()
            await email_service.send_verification_email(email=user.email)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified. Please verify your email to login.")
        
        if HashHelper.verify_password(plain_password=data.password, hashed_password=user.password):
            user.token_version += 1
            token = AuthHandler.sign_jwt(user_id=user.id, token_version=user.token_version)
            if token:
                return UserWithToken(token_type="Bearer", token=token, expire_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process request")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please check your credentials.")
    
    # Get user info by user id
    def get_user_by_id(self, user_id: int):
        user = self.repo.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not available")
    
    # Get user info by email
    def verify_email(self, email: str):
        user = self.repo.get_user_by_email(email=email)
        print(user.is_verified)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token payload.")

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        if user.is_verified:
            return {"message": "Email is already verified."}
        
        user.is_verified = True
        user.verified_at =  datetime.utcnow()
        
        return user
    
