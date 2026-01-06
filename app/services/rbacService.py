from app.repository.rbacRepo import RbacRepository
from app.db.schema.rbac import RoleInCreate, RoleInOutput, PermissionInCreate, PermissionInOutput, AssignPermissionToRoleInput
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class RbacService:
    def __init__(self, session= Session):
        self.rbac_repo = RbacRepository(session=session)

    # Create new role
    def create_role(self, data: RoleInCreate) -> RoleInOutput:
        if self.rbac_repo.role_exist_by_name(name=data.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This role already exists")

        role = self.rbac_repo.create_role(data)

        return role
    
    # Create new permission
    def create_permission(self, data: PermissionInCreate) -> PermissionInOutput:
        if self.rbac_repo.permission_exist_by_code(code=data.code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This permission already exists")
        
        permission = self.rbac_repo.create_permission(data)

        return permission
    
    # Assign Permission to Role
    def assign_permission_to_role(self, data: AssignPermissionToRoleInput) -> None:
        role = self.rbac_repo.get_role_by_id(role_id=data.role_id)
        permission = self.rbac_repo.get_permission_by_id(permission_id=data.permission_id)

        if not role or not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or permission not found")
        
        if permission in role.permissions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already assigned to role")
        
        self.rbac_repo.assign_permission_to_role(role=role, permission=permission)

