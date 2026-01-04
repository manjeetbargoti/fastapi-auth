from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

JWT_SECRET = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
TOKEN_EXPIRES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
EMAIL_TOKEN_EXPIRES = settings.EMAIL_TOKEN_EXP_MIN
# TOKEN_EXPIRES = 1

class AuthHandler(object):
    @staticmethod
    def sign_jwt(user_id: int, expires_delta: timedelta | None = None) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=int(TOKEN_EXPIRES))
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expire")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
        
    @staticmethod
    def generate_email_token(email: str) -> str:
        payload = {
            "sub": email,
            "purpose": "email_verification",
            "exp": datetime.utcnow() + timedelta(minutes=int(EMAIL_TOKEN_EXPIRES))
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def verify_email_token(token: str) -> dict:
        try:
            decoded_email_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            if decoded_email_token.get("purpose") != "email_verification":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email token purpose")
            
            return decoded_email_token
        except jwt.ExpiredSignatureError:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email token expired")
        except jwt.InvalidTokenError:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email token")
        except Exception as error:
            print("unable to decode the email token")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
        
