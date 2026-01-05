from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from app.core.security.authHandler import AuthHandler
from app.services.userService import UserService
from app.db.database import get_db
from app.db.schema.user import GetCurrentUserOutput
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

AUTH_PREFIX = 'Bearer '
security = HTTPBearer()

def get_current_user(
        session: Session = Depends(get_db), 
        authorization: Optional[str] = Header(default=None)) -> GetCurrentUserOutput:

    auth_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Invalid authentication credentials"
    )

    # Authorization header present
    if not authorization:
        raise auth_exception
    
    # Correct prefix
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    valid_token = authorization[len(AUTH_PREFIX):].strip()
    if not valid_token:
        raise auth_exception

    # Decode JWT token
    payload = AuthHandler.decode_jwt(token=valid_token)
    if not payload:
        raise auth_exception
    
    # Validate required claims
    user_id = payload.get("user_id")
    token_version = payload.get("token_version")

    if user_id is None or token_version is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or outdated token")
    
    # Load user from DB
    user = UserService(session=session).get_user_by_id(user_id)
    if not user:
        raise auth_exception
    
    # Token invalidation check
    if token_version != user.token_version:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")

    return user

# verify authorization token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = AuthHandler.decode_jwt(token=token)
        return payload
    except Exception as error:
        raise error
    
