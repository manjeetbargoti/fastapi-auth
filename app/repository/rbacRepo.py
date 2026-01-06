from .base import BaseRepository
from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.user import User
from app.db.schema.rbac import RoleInCreate, PermissionInCreate
from sqlalchemy import func

class RbacRepository(BaseRepository):
    #-----------------#
    # Create new role #
    #-----------------#
    def create_role(self, role_data: RoleInCreate):
        newRole = Role(
            name= role_data.name
        )

        self.session.add(instance=newRole)
        self.session.flush()
        self.session.refresh(instance=newRole)

        return newRole
    
    # Check role exist by name
    def role_exist_by_name(self, name: str) -> bool|None:
        role = self.session.query(Role).filter(func.lower(Role.name) == func.lower(name)).first()
        return bool(role)

    # Get role by name
    def get_role_by_name(self, name: str) -> Role|None:
        role = self.session.query(Role).filter(func.lower(Role.name) == func.lower(name)).first()
        return role
    
    # Get role by id
    def get_role_by_id(self, role_id: int) -> Role|None:
        role = self.session.get(Role, role_id)
        return role
    
    #-----------------------#
    # Create new permission #
    #-----------------------#
    def create_permission(self, perm_data: PermissionInCreate):
        newPermission = Permission(
            code = perm_data.code
        )

        self.session.add(instance=newPermission)
        self.session.flush()
        self.session.refresh(instance=newPermission)

        return newPermission
    
    # Check permission exist by code
    def permission_exist_by_code(self, code: str) -> bool|None:
        permission = self.session.query(Permission).filter(func.lower(Permission.code) == func.lower(code)).first()
        return bool(permission)

    # Get permission by code
    def get_permission_by_code(self, code: str) -> Permission|None:
        permission = self.session.query(Permission).filter(func.lower(Permission.code) == func.lower(code)).first()
        return permission
    
    # get permission by id
    def get_permission_by_id(self, permission_id: int) -> Permission|None:
        permission = self.session.get(Permission, permission_id)
        return permission
    
    #----------------------------#
    # Assign Permissions to Role #
    #----------------------------#
    def assign_permission_to_role(self, role: Role, permission: Permission) -> None:

        role.permissions.append(permission)
        self.session.add(role)


