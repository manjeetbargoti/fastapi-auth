from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(100), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False, index=True)  # 1 for verified, 0 for not verified
    verified_at = Column(DateTime, nullable=True)
