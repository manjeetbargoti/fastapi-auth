from pydantic import BaseModel

class RoleInCreate(BaseModel):
    name: str

class RoleInOutput(BaseModel):
    id: int
    name: str

class PermissionInCreate(BaseModel):
    code: str

class PermissionInOutput(BaseModel):
    id: int
    code: str

class AssignPermissionToRoleInput(BaseModel):
    role_id: int
    permission_id: int

