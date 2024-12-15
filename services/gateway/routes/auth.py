import requests
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils import AUTH_SERVICE

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register")
async def register_user(request: Request):
    user_data = await request.json()
    response = requests.post(f"{AUTH_SERVICE}/register", json=user_data)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.post("/login")
async def login_for_access_token(request: Request):
    form_data = await request.json()
    response = requests.post(f"{AUTH_SERVICE}/login", data=form_data)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.post("/logout")
async def logout(request: Request):
    token = request.headers.get("Authorization").split()[1]
    response = requests.post(f"{AUTH_SERVICE}/logout", headers={"Authorization": f"Bearer {token}"})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.get("/profile")
async def get_current_user(request: Request):
    token = request.headers.get("Authorization").split()[1]
    response = requests.get(f"{AUTH_SERVICE}/profile", headers={"Authorization": f"Bearer {token}"})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.put("/profile")
async def update_profile(request: Request):
    user_data = await request.json()
    token = request.headers.get("Authorization").split()[1]
    response = requests.put(f"{AUTH_SERVICE}/profile", json=user_data, headers={"Authorization": f"Bearer {token}"})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.put("/profile/change-password")
async def change_password(request: Request):
    password_data = await request.json()
    token = request.headers.get("Authorization").split()[1]
    response = requests.put(f"{AUTH_SERVICE}/profile/change-password", json=password_data, headers={"Authorization": f"Bearer {token}"})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.post("/forgot-password")
async def forgot_password(request: Request):
    data = await request.json()
    response = requests.post(f"{AUTH_SERVICE}/forgot-password", json=data)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.post("/reset-password")
async def reset_password(request: Request):
    reset_data = await request.json()
    response = requests.post(f"{AUTH_SERVICE}/reset-password", json=reset_data)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.get("/profile/verify-email")
async def activate_profile(token: str, email: str):
    response = requests.get(f"{AUTH_SERVICE}/profile/verify-email?token={token}&email={email}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

@auth_router.delete("/profile/delete")
async def delete_profile(request: Request):
    token = request.headers.get("Authorization").split()[1]
    response = requests.delete(f"{AUTH_SERVICE}/profile/delete", headers={"Authorization": f"Bearer {token}"})
    return JSONResponse(content=response.json(), status_code=response.status_code)