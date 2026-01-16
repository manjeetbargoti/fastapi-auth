from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db
from app.db.schema.user import UserInCreate, UserInUpdate, UserOutput, UserWithToken
from sqlalchemy.orm import Session
from app.utils.protectRoute import verify_token
from app.db.models.user import User
from app.utils.permission_dependency import require_permissions
from app.utils.protectRoute import get_current_user
from app.services.userService import UserService

userRouter = APIRouter(
    prefix="/admin",
    tags=['Users'],
    dependencies= [Depends(verify_token)]
)

#=================#
# Get User's list #
#=================#
@userRouter.post("/users", response_model=list[UserOutput])
def get_users(skip: int = 0, limit: int = 25, session: Session = Depends(get_db), _ = Depends(require_permissions("user:list"))):
    return UserService(session=session).users_list(skip=skip, limit=limit)

#=================#
# Get User detail #
#=================#
@userRouter.post("/user/{user_id}/detail", response_model=UserOutput)
def user_detail(user_id: int, session: Session = Depends(get_db), _ = Depends(require_permissions("user:view"))):
    try:
        user = UserService(session=session).get_user_by_id(user_id=user_id)

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
#=================#
# Create new user #
#=================#
@userRouter.post("/user/create", status_code=201, response_model=UserOutput)
def create_user(user_data=UserInCreate, session: Session = Depends(get_db), _ = Depends(require_permissions("user:create"))):
    try:
        print(user_data)
        user = UserService(session=session).create_user(user_data=user_data)
        session.commit()

        return user
    except Exception:
        session.rollback()
        raise

    
#=============#
# Update user #
#=============#
@userRouter.patch("/user/{user_id}/update", response_model=UserOutput)
def update_user(user_id: int, user_data: UserInUpdate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user), _ = Depends(require_permissions("user:update"))):
    
    is_admin = False

    # Admin override
    try:
        require_permissions("user:update")(current_user)
        is_admin = True
    except Exception:
        pass

    try:
        user = UserService(session=session).update_user(
            user_id=user_id,
            data=user_data,
            is_admin=is_admin,
            current_user_id=current_user.id
        )

        session.commit()
        session.refresh(instance=user)
        return user
    except Exception:
        session.rollback()
        raise

#=============#
# Delete user #
#=============#
@userRouter.delete("/user/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user), _ = Depends(require_permissions("user:delete"))):
    try:
        UserService(session=session).delete_user(
            user_id=user_id,
            current_user_id=current_user.id
            )
        session.commit()

        return {"message": "user deleted successfully"}
    except Exception:
        session.rollback()
        raise

