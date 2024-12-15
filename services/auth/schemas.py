from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class EmailStatus(str, Enum):
    pending_verification = "Pending Verification"
    verified = "Verified"

# request body for user registration
class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None
    birthdate: Optional[date] = None

    @field_validator("birthdate")
    def check_birthdate(cls, value):
        if value:
            value = value.isoformat()
        return value

# request body for updating user
class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None
    birthdate: Optional[date] = None
    image_url: Optional[str] = None
    about_me: Optional[str] = None

    @field_validator("birthdate")
    def check_birthdate(cls, value):
        if value:
            value = value.isoformat()
        return value

# request body for user login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# request body for user profile
class UserProfileRequest(BaseModel):
    username: str
    email: EmailStr
    gender: Optional[Gender] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[date] = None
    image_url: Optional[str] = None
    about_me: Optional[str] = None
    

# request body for verifying user email
class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr

# request body for forgot password
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    password: str

# request body for reset password
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    password: str

