from app.repository.userRepo import UserRepository
from app.db.schema.user import UserInCreate, UserOutput, UserInUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security.hashHelper import HashHelper

class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session=session)

    #=================#
    # Get user's list #
    #=================#
    def users_list(self, skip: int = 0, limit: int = 25):
        users = self.repo.users_list(skip=skip, limit=limit)
        return users

    #==========================#
    # Get user info by user id #
    #==========================#
    def get_user_by_id(self, user_id: int):
        user = self.repo.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #=================#
    # Create new user #
    #=================#
    def create_user(self, user_data: UserInCreate) -> UserOutput:
        print(user_data)
        if self.repo.user_exist_by_email(email=user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please login. An account with this email already exist")
        
        hash_password = HashHelper.get_password_hash(plain_password=user_data.password)
        user_data.password = hash_password

        roles = self.repo.get_roles_by_name(role_names=user_data.role_names)

        if len(roles) != len(set(user_data.role_names)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more roles are invalid")

        user_data.roles = roles
        user = self.repo.create_user(user_data=user_data)
        return user

    #=============#
    # Update user #
    #=============#
    def update_user(self, user_id: int, data: UserInUpdate, current_user_id: int, is_admin: bool) -> UserOutput:
        user = self.repo.get_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # normal user update only themselves
        if not is_admin and user.id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot update this user")
        
        user = self.repo.update_user(user, data)

        updated_data = data.model_dump(exclude_unset=True)

        # Invalidate token if email changed
        if "email" in updated_data:
            user.token_version += 1

        return user
    
    #=============#
    # Delete user #
    #=============#
    def delete_user(self, user_id: int, current_user_id: int) -> None:
        user = self.repo.get_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Prevent self-delete
        if user.id == current_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your own account")
        
        self.repo.delete_user(user)
    
