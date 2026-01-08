from sqlalchemy.orm import Session
from datetime import datetime
import os

from app.db.models.role import Role
from app.db.models.user import User
from app.db.models.permission import Permission
from app.core.security.hashHelper import HashHelper
from app.core.config import settings

class RbacSeedService:
    
    def __init__(self, session: Session):
        self.session = session

    def seed(self):
        # Permissions
        perm_codes = [
            "rbac:manage",
            "user:create",
            "user:view",
            "user:update",
            "user:delete",
            "user:list"
        ]

        permissions: dict[str, Permission] = {}
        for code in perm_codes:
            perm = self.session.query(Permission).filter_by(code=code).first()
            if not perm:
                perm = Permission(code=code)
                self.session.add(perm)
                self.session.commit()
            permissions[code] = perm

        self.session.flush()

        # Roles
        roles: dict[str ,Role] = {}

        for role_name in ["admin", "user"]:
            role = (
                self.session.query(Role).filter(Role.name == role_name).first()
            )

            if not role:
                role = Role(name=role_name)
                self.session.add(role)

            roles[role_name] = role

        self.session.flush()

        # Assign permissions
        roles["admin"].permissions = list(permissions.values())
        roles["user"].permissions = [permissions["user:view"]]

        self.session.flush()

        # Seed Users
        self._seed_user(
            first_name=settings.SEED_ADMIN_FIRST_NAME,
            last_name=settings.SEED_ADMIN_LAST_NAME,
            email=settings.SEED_ADMIN_EMAIL,
            password=settings.SEED_ADMIN_PASSWORD,
            is_admin=True,
            role=roles["admin"]
        )

        self._seed_user(
            first_name=settings.SEED_USER_FIRST_NAME,
            last_name=settings.SEED_USER_LAST_NAME,
            email=settings.SEED_USER_EMAIL,
            password=settings.SEED_USER_PASSWORD,
            is_admin=False,
            role=roles["user"]
        )

        self.session.commit()

    # Helpers
    def _seed_user(self, email:str, password, first_name, last_name, role: Role, is_admin: bool):
        user = self.session.query(User).filter(User.email==email).first()

        if user:
            return
        
        user = User(
            email=email,
            password=HashHelper.get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_verified=True,
            is_admin=is_admin,
            verified_at=datetime.utcnow(),
            token_version=0
        )

        user.roles.append(role)
        self.session.add(user)
