from fastapi import APIRouter
from starlette.responses import JSONResponse

from utils import send_message, DIFF_EXPRESSION_QUEUE

diffexpr_router = APIRouter(prefix="/diff_expression_analyse", tags=["differential expression analyses"])

@diffexpr_router.get("/")
def send_diffexpr_request(counts_file: str, metadata: str, condition: str, user_id: int):
    
    message = {
        "file_name": counts_file,
        "metadata": metadata,
        "condition": condition,
        "user_id": user_id
    }
    send_message(message, DIFF_EXPRESSION_QUEUE)

    return JSONResponse(content={"message": "Operation of differential expression analyse started successfully, the result will be available soon"}, status_code=200)

