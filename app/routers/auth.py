from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from app.db.schema.user import UserInCreate, UserInLogin, UserOutput, UserWithToken, GetCurrentUserOutput
from sqlalchemy.orm import Session
from app.services.userService import UserService
from app.services.emailService import EmailService
from app.utils.protectRoute import get_current_user
from pydantic import EmailStr

authRouter = APIRouter(tags=["auth"], prefix="/auth")

#------------#
# User login #
#------------#
@authRouter.post("/login", status_code=200, response_model=UserWithToken)
async def login(loginDetails: UserInLogin, session: Session = Depends(get_db)):
    try:
        result = await UserService(session=session).login(data=loginDetails)
        session.commit()
        return result
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(error))

#-------------------#
# User registration #
#-------------------#
@authRouter.post("/signup", status_code=201, response_model=UserOutput)
async def signup(signupDetails: UserInCreate, session: Session = Depends(get_db)):
    try:
        user = await UserService(session=session).signup(data=signupDetails)
        session.commit()

        return user
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(error))

#------------------#
# Get current user #
#------------------#
@authRouter.post("/get-current-user", response_model=GetCurrentUserOutput)
def get_current_user(user: UserOutput = Depends(get_current_user)):
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
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
#--------------------------# 
# Email verification route #
#--------------------------#
@authRouter.get("/verify-email")
def verify_email(token: str, session: Session = Depends(get_db)):
    try:
        decoded_token = EmailService.verify_email_token(token=token)
        print(decoded_token)
        email = decoded_token.get("sub")
        
        user = UserService(session=session).verify_email(email=email)
        
        session.commit()
        return {"message": "Email verified successfully."}
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(error))
    