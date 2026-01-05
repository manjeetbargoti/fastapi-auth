from fastapi import Depends, HTTPException, status
from app.utils.protectRoute import get_current_user
from app.utils.permission_resolver import get_user_permissions

def require_permissions(*required_permissions: set):
    def checker(user = Depends(get_current_user)):
        user_permissions = get_user_permissions(user)

        missing = set(required_permissions) - user_permissions

        if missing:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing permissions: {', '.join(missing)}")
        
        return user
    
    return checker