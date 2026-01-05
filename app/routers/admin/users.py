from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from app.db.schema.user import UserInCreate, UserInUpdate, UserOutput, UserWithToken
from sqlalchemy.orm import Session
from app.utils.protectRoute import verify_token
from app.db.models.user import User
from app.utils.permission_dependency import require_permissions

userRouter = APIRouter(
    prefix="/admin",
    tags=['Admin','Users'],
    dependencies= [Depends(verify_token)]
)

# User list route
@userRouter.post("/users", response_model=list[UserOutput])
def get_users(skip: int = 0, limit: int = 25, session: Session = Depends(get_db), _ = Depends(require_permissions("user:view"))):
    return session.query(User).offset(skip).limit(limit).all()


@userRouter.post("/user/{user_id}/detail", response_model=UserOutput)
def user_detail(user_id: int, session: Session = Depends(get_db)):
    try:
        user = session.query(User).filter_by(id=user_id).first()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
