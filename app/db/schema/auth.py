from pydantic import EmailStr, BaseModel, Field
from typing import Annotated, Optional

class RegisterUser(BaseModel):
    first_name: Annotated[str, Field(..., max_length=100)]
    last_name: Annotated[str, Field(..., max_length=100)]
    email: Annotated[EmailStr, Field(..., max_length=255)]
    password: Annotated[str, Field(..., min_length=6, max_length=255)]

class LoginUser(BaseModel):
    email: Annotated[EmailStr, Field(..., max_length=255)]
    password: Annotated[str, Field(..., min_length=6, max_length=255)]

class RegisterOutput(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class LoginOutput(BaseModel):
    token_type: Optional[str] = None
    token: Optional[str] = None
    expire_in_min: Optional[int] = None

