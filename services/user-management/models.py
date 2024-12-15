import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, Date
from database import Base

class Gender(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class EmailStatus(enum.Enum):
    pending_verification = "Pending Verification"
    verified = "Verified"

class User(Base):
    __tablename__ = "users"

    user_id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password: str = Column(String(255), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False, index=True)
    gender: Gender = Column(Enum(Gender))
    first_name: str = Column(String(50))
    last_name: str = Column(String(50))
    birthdate: datetime = Column(Date)
    image_url: str = Column(String(255))
    about_me: str = Column(Text)
    is_deleted: bool = Column(Boolean, default=False, nullable=False)
    email_status: EmailStatus = Column(Enum(EmailStatus), nullable=False, default=EmailStatus.pending_verification)
    verified_at: datetime = Column(DateTime, nullable=True, default=None)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    last_updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
