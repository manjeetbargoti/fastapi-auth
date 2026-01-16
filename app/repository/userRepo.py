from .base import BaseRepository
from app.db.models.user import User
from app.db.models.role import Role
from app.db.schema.user import UserInCreate, UserInUpdate

class UserRepository(BaseRepository):

    # Get roles by name
    def get_roles_by_name(self, role_names: list):
        roles = self.session.query(Role).filter(Role.name.in_(role_names)).all()
        return roles

    #=============#
    # Create user #
    #=============#
    def create_user(self, user_data: UserInCreate):

        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=user_data.password
        )

        user.roles.extend(user_data.roles)

        self.session.add(instance=user)
        self.session.flush()
        self.session.refresh(instance=user)

        return user
    
    #===========================#
    # Check user exist by email #
    #===========================#
    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)
    
    #===================#
    # Get user by email #
    #===================#
    def get_user_by_email(self, email: str) -> User | None:
        user = self.session.query(User).filter_by(email=email).first()
        return user
    
    #=================#
    # Get user's list #
    #=================#
    def users_list(self, skip: int = 0, limit: int = 25):
        users =  self.session.query(User).offset(skip).limit(limit).all()
        return users

    #================#
    # Get user by id #
    #================#
    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.get(User, user_id)
        return user
    
    #=============#
    # Delete user #
    #=============#
    def delete_user(self, user: User) -> None:
        self.session.delete(user)

    #=============#
    # Update user #
    #=============#
    def update_user(self, user: User, data: UserInUpdate):
        data = data.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(user, key, value)

        return user

