from .base import BaseRepository
from app.db.models.user import User
from app.db.schema.user import UserInCreate

class UserRepository(BaseRepository):

    #-------------#
    # Create user #
    #-------------#
    def create_user(self, user_data: UserInCreate):
        newUser = User(**user_data.model_dump(exclude_none=True))

        self.session.add(instance=newUser)
        self.session.flush()
        self.session.refresh(instance=newUser)

        return newUser
    
    # Check user exist by email
    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)
    
    # Get user by email
    def get_user_by_email(self, email: str) -> User | None:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    # Get user by id
    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.get(User, user_id)
        return user
    
    #-------------#
    # Delete user #
    #-------------#
    def delete_user(self, user: User) -> None:
        self.session.delete(user)

    #-------------#
    # Update user #
    #-------------#
    def update_user(self, user: User, data: dict) -> None:
        for key, value in data.items():
            setattr(user, key, value)

