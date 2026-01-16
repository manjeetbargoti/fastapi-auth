from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db
from app.db.schema.user import GetCurrentUserOutput
from app.db.schema.auth import RegisterUser, RegisterOutput, LoginUser, LoginOutput
from sqlalchemy.orm import Session
from app.services.authService import AuthService
from app.services.emailService import EmailService
from app.utils.protectRoute import get_current_user
from pydantic import EmailStr

authRouter = APIRouter(tags=["auth"], prefix="/auth")

#------------#
# User login #
#------------#
@authRouter.post("/login", status_code=200, response_model=LoginOutput)
async def login(data: LoginUser, session: Session = Depends(get_db)):
    try:
        result = await AuthService(session=session).login_user(data=data)
        session.commit()
        return result
    except Exception:
        session.rollback()
        raise

#-------------------#
# User registration #
#-------------------#
@authRouter.post("/signup", status_code=201, response_model=RegisterOutput)
async def signup(data: RegisterUser, session: Session = Depends(get_db)):
    try:
        user = await AuthService(session=session).register_user(data=data)
        session.commit()

        return user
    except Exception:
        session.rollback()
        raise

#------------------#
# Get current user #
#------------------#
@authRouter.post("/get-current-user", response_model=GetCurrentUserOutput)
def get_current_user(user: GetCurrentUserOutput = Depends(get_current_user)):
    return user

#-------------------------#
# Send verification email #
#-------------------------#
@authRouter.post("/send-verification-email")
async def send_verification_email(email: EmailStr):
    try:
        email_service = EmailService()
        await email_service.send_verification_email(email=email)
        return {"message": "Verification email sent."}
    except Exception:
        raise
    
#--------------------------# 
# Email verification route #
#--------------------------#
@authRouter.get("/verify-email")
def verify_email(token: str, session: Session = Depends(get_db)):
    try:
        decoded_token = EmailService.verify_email_token(token=token)

        email = decoded_token.get("sub")
        
        AuthService(session=session).verify_email(email=email)
        
        session.commit()
        return {"message": "Email verified successfully."}
    except Exception:
        session.rollback()
        raise
    