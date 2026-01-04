from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.services.userService import UserService
from app.db.database import get_db
from app.db.schema.user import GetCurrentUserOutput
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.repository.userRepo import UserRepository

AUTH_PREFIX = 'Bearer '
security = HTTPBearer()

def get_current_user(
        session: Session = Depends(get_db), 
        authorization: Annotated[str, Header()] = None) -> GetCurrentUserOutput:

    auth_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Invalid Authentication Credentials"
    )

    if not authorization:
        raise auth_exception
    
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    valid_token = authorization[len(AUTH_PREFIX):]

    payload = AuthHandler.decode_jwt(token=valid_token)

    if payload and payload["user_id"]:
        try: 
            user = UserService(session=session).get_user_by_id(payload["user_id"])
            return GetCurrentUserOutput(
                id = user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_verified=user.is_verified
            )
        except Exception as error:
            raise error
    
    raise auth_exception

# verify authorization token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = AuthHandler.decode_jwt(token=token)
        return payload
    except Exception as error:
        raise error
    
