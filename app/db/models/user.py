from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.models.associations import user_roles

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=False, index=True)  # 'True' for active, 'False' for not active
    is_verified = Column(Boolean, default=False, index=True)  # 'True' for verified, 'False' for not verified
    is_admin = Column(Boolean, default=False) # 'True' for admin, 'False' for not admin

    verified_at = Column(DateTime, nullable=True)
    token_version = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy="joined")