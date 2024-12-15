from fastapi import APIRouter
from starlette.responses import JSONResponse

from utils import send_message, QUANTIFICATION_QUEUE

quantification_router = APIRouter(prefix="/quantification_features", tags=["quantification features"])

@quantification_router.get("/")
def send_quantification_request(bam_file: str, user_id: int, annotation_file: str = None):

    message = {
        "bam_file": bam_file,
        "annotation_file": annotation_file,
        "user_id": user_id
    }
    send_message(message, QUANTIFICATION_QUEUE)

    return JSONResponse(content={"message": "Quantification operation started successfully, the result will be available soon"}, status_code=200)

