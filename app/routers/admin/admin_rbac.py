from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schema.rbac import RoleInCreate, RoleInOutput, PermissionInCreate, PermissionInOutput, AssignPermissionToRoleInput, AssignRoleToUserInput
from app.services.rbacService import RbacService
from app.utils.permission_dependency import require_permissions

rbacRouter = APIRouter(prefix="/admin", tags=["RBAC"])

@rbacRouter.post("/roles/create", response_model=RoleInOutput)
def create_role(data: RoleInCreate, session: Session = Depends(get_db), _ = Depends(require_permissions("rbac:manage"))):
    try:
        role = RbacService(session=session).create_role(data=data)
        session.commit()

        return role
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
    
@rbacRouter.post("/permissions/create", response_model=PermissionInOutput)
def create_permission(data: PermissionInCreate, session: Session = Depends(get_db), _ = Depends(require_permissions("rbac:manage"))):
    try:
        permission = RbacService(session=session).create_permission(data=data)
        session.commit()

        return permission
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@rbacRouter.post("/roles/assign-permission")
def assign_permission_to_role(data: AssignPermissionToRoleInput, session: Session = Depends(get_db), _ = Depends(require_permissions("rbac:manage"))):
    try:
        RbacService(session=session).assign_permission_to_role(data=data)
        session.commit()

        return {"message": "Permission assign successfully"}
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
    
@rbacRouter.post("/user/assign-role")
def assign_role_to_user(data: AssignRoleToUserInput, session: Session = Depends(get_db), _ = Depends(require_permissions("rbac:manage"))):
    try:
        RbacService(session=session).assign_role_to_user(data=data)
        session.commit()

        return {"message": "Role assign successfully"}
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
