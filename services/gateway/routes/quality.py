from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import Union, List

from utils import send_message, QUALITY_CONTROL_QUEUE

quality_router = APIRouter(prefix="/quality-control", tags=["quality control"])

@quality_router.post("/")
def send_quality_control_request(files: Union[str, List[str]], user_id):
    message = {"files": files, "user_id": user_id}
    send_message(message, QUALITY_CONTROL_QUEUE)

    return JSONResponse(content={"message": "quality control operation started successfully, the result will be available soon"}, status_code=200)