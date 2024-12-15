from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime, date


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class EmailStatus(str, Enum):
    pending_verification = "Pending Verification"
    verified = "Verified"

# Pydantic model for User
class UserBase(BaseModel):
    email: EmailStr
    gender: Optional[Gender] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[date] = None
    image_url: Optional[str] = None
    about_me: Optional[str] = None

    # @field_validator("birthdate")
    # def check_birthdate(cls, value):
    #     if value:
    #         value = value.strptime("%d/%m/%y")
    #     return value

class UserCreate(UserBase):
    username: str
    hashed_password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    hashed_password: Optional[str] = None

class UserInDB(UserBase):
    user_id: int
    is_deleted: bool
    email_status: EmailStatus
    verified_at: datetime
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True  # Updated key

# Pydantic model for User Response
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    gender: Optional[Gender] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[date] = None
    image_url: Optional[str] = None
    about_me: Optional[str] = None
    is_deleted: bool
    email_status: EmailStatus
    verified_at: Optional[datetime] = None
    created_at: datetime
    last_updated_at: datetime

class LoginResponse(BaseModel):
    user_id: int
    username: str
    email: str
    hashed_password: str
    is_deleted: bool
    email_status: EmailStatus
    created_at: datetime
    last_updated_at: datetime