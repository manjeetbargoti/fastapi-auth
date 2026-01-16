from pydantic import EmailStr, BaseModel, Field
from typing import Union, List, Annotated

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
    first_name: Annotated[str, Field(..., max_length=100)]
    last_name: Annotated[str, Field(..., max_length=100)]
    email: Annotated[EmailStr, Field(..., max_length=255)]
    password: Annotated[str, Field(..., min_length=6, max_length=255)]
    role_names: List[str]

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
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    is_verified: Union[bool, None] = None
    verified_at: Union[str, None] = None

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token_type: str
    token: str
    expire_in: int



