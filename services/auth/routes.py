from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
import schemas, services

router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"],
    responses = {404: {"description": "Not found"}}
)

@router.get("/")
async def root():
    return {"message": "Welcome to the Authentication Service"}

@router.post("/register")
async def register_user(user: schemas.RegisterUserRequest):
    user = await services.create_user_account(user)
    if user is None:
        raise HTTPException(status_code=400, detail="Email or Username already registered")
    return user

@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = services.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=int(services.ACCESS_TOKEN_EXPIRE_MINUTES))
    data = {"sub": user["email"]}
    access_token = services.create_access_token(data=data, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(services.oauth2_scheme),
           current_user: dict = Depends(services.get_current_user)):
    return {"message": "Logged out successfully"}

@router.get("/profile")
def get_current_user(current_user: dict = Depends(services.get_current_user)):
    return current_user

@router.put("/profile")
def update_profile(user_data: schemas.UpdateUserRequest, current_user: dict = Depends(services.get_current_user)):
    updated_user = services.update_user(current_user["email"], user_data)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.put("/profile/change-password")
def change_password(password_data: schemas.ChangePasswordRequest, current_user: dict = Depends(services.get_current_user)):
    updated_profile = services.change_password(current_user["email"], password_data.password)
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    # return updated_profile
    return {"message": "Password changed successfully"}

@router.post("/forgot-password")
async def forgot_password(data: schemas.ForgotPasswordRequest):
    await services.initiate_password_reset(data.email)
    return {"message": "Password reset link sent"}

@router.post("/reset-password")
def reset_password(reset_data: schemas.ResetPasswordRequest):
    services.reset_password(reset_data.email, reset_data.token, reset_data.password)
    return {"message": "Password reset successfully"}

@router.get("/profile/verify-email")
def activate_profile(token:str, email: str):
    services.verify_email(token, email)
    return {"message": "Profile Activated"}

@router.delete("/profile/delete")
def delete_profile(current_user: dict = Depends(services.get_current_user)):
    services.delete_user(current_user["email"])
    return {"message": "Profile Deleted"}

