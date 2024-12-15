import logging
import os
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import unquote_plus

import dotenv
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import schemas
from rabbit_config import send_email_verification, send_password_reset_email
from security import hash_password, is_password_strong_enough, verify_password

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def create_user_account(user: schemas.RegisterUserRequest):
    if not is_password_strong_enough(user.password):
        raise HTTPException(status_code=400, detail="Please provide a strong password.")
    hashed_password = hash_password(user.password)
    user_obj = dict()
    for key, value in user.dict().items():
        if key == "password":
            user_obj["hashed_password"] = hashed_password
        else:
            user_obj[key] = value
    response = requests.post(f"{os.getenv('USER_MANAGEMENT_SERVICE')}/", json=user_obj)
    response_json = response.json()
    if response.status_code == 200:
        # create jwt token and send email verification
        token_data = {"sub": user.email}
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        token = create_access_token(token_data, expires_delta=access_token_expires)
        msg = await send_email_verification(user.email, token)
        return msg
        # return response_json
    else:
        raise HTTPException(status_code=400, detail=response_json.get("detail"))

def authenticate_user(email: str, password: str):
    user = get_logged_user(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    if user["is_deleted"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user["email_status"] == "Pending Verification":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is not verified. Please check your email inbox to verify your account.")
    return user

def get_logged_user(email: str):
    if email:
        response = requests.get(f"{os.environ.get('USER_MANAGEMENT_SERVICE')}/email/login/{email}")
        response_json = response.json()
        if response.status_code == 200:
            return response_json
        else:
            raise HTTPException(status_code=404, detail="User not found")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        expiration = payload.get("exp")
        if email is None:
            raise credentials_exception
        # convert expiration (int) to datetime object
        expiration_datetime = datetime.fromtimestamp(expiration)
        if expiration_datetime < datetime.utcnow():
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_logged_user(email)
    user = get_user(user["user_id"])
    if user is None:
        raise credentials_exception
    return user

def get_user(user_id: int):
    if user_id:
        response = requests.get(f"{os.environ.get('USER_MANAGEMENT_SERVICE')}/id/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=404, detail="User not found")

def update_user(email: str, user_data: schemas.UpdateUserRequest):
    user_data.email = email
    # delete all none values from user_data
    user_data = {key: value for key, value in user_data.dict().items() if value is not None}
    response = requests.put(f"{os.environ.get('USER_MANAGEMENT_SERVICE')}/", json=user_data)
    response_json = response.json()
    if response.status_code == 200:
        return response_json
    else:
        raise HTTPException(status_code=404, detail=response_json.get("detail"))

def change_password(email: str, password_data: str):
    if not is_password_strong_enough(password_data):
        raise HTTPException(status_code=400, detail="Please provide a strong password.")
    user = get_logged_user(email)
    user["hashed_password"] = hash_password(password_data)
    response = requests.put(f"{os.environ.get('USER_MANAGEMENT_SERVICE')}/", json=user)
    response_json = response.json()
    if response.status_code == 200:
        return response_json
    else:
        raise HTTPException(status_code=404, detail=response_json.get("detail"))

async def initiate_password_reset(email: str):
    try:
        user = get_logged_user(email)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Email not registered with us.")

    if user["email_status"] == "Pending Verification":
        raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")

    token_data = {"sub": email}
    token = create_access_token(token_data)

    msg = await send_password_reset_email(email, token)
    return msg

def verify_token(token: str):
    try:
        token = str(unquote_plus(token))  # URL decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        expiration = payload.get("exp")
        expiration_datetime = datetime.fromtimestamp(expiration)
        if expiration_datetime < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token expired")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return email
    except JWTError as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="Invalid token")

def reset_password(email: str, token: str, password: str):
    token_email = verify_token(token)
    if email != token_email:
        raise HTTPException(status_code=400, detail="Invalid token")
    response = change_password(email, password)
    return response

def verify_email(token: str, email: str):
    token_email = verify_token(token)
    if email != token_email:
        raise HTTPException(status_code=400, detail="Invalid token")
    response = requests.get(f"{os.environ.get('USER_MANAGEMENT_SERVICE')}/verify/{email}")
    response_json = response.json()
    if response.status_code == 200:
        return response_json
    else:
        raise HTTPException(status_code=404, detail=response_json.get("detail"))

def delete_user(email: str):
    response = requests.delete(f"{os.environ.get('USER_MANAGEMENT_SERVICE')}/{email}")
    response_json = response.json()
    if response.status_code == 200:
        return response_json
    else:
        raise HTTPException(status_code=404, detail=response_json.get("detail"))
