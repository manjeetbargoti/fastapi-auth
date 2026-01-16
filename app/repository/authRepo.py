from .base import BaseRepository
from app.db.models.user import User
from app.db.schema.auth import RegisterOutput, RegisterUser, LoginUser
from sqlalchemy import func

class AuthRepository(BaseRepository):
    # Check user exists by email
    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter(func.lower(User.email) == func.lower(email)).first()
        return bool(user)

    # Get user by email
    def get_user_by_email(self, email: str) -> User | None:
        user = self.session.query(User).filter(func.lower(User.email) == func.lower(email)).first()
        return user
    
    # Get user by id
    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.get(User, user_id)
        return user

    # Register User
    def register_user(self, user_data: RegisterUser):
        newUser = User(**user_data.model_dump(exclude_none=True))

        self.session.add(instance=newUser)
        self.session.flush()
        self.session.refresh(instance=newUser)

        return newUser
    