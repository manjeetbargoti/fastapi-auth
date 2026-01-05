from pydantic import EmailStr, BaseModel
from typing import Union, List

class PermissionOut(BaseModel):
    id: int
    code: str
        
class RoleOut(BaseModel):
    id: int
    name: str
    permissions: List[PermissionOut] = []

class UserRole(BaseModel):
    id: int
    name: str

class UserInCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    # is_verified: Union[bool, None] = False

class UserOutput(BaseModel):
    id: Union[int, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    is_verified: Union[bool, None] = None
    roles: List[UserRole] = []

class GetCurrentUserOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_verified: Union[bool, None] = None,
    roles: List[UserRole] = []

class UserInUpdate(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    is_verified: Union[bool, None] = None
    verified_at: Union[str, None] = None

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token_type: str
    token: str
    expire_in: int

class Config:
    from_attributes = True



