from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import Union, List

from utils import send_message, ALIGNMENT_FASTQ_QUEUE

alignment_router = APIRouter(prefix="/alignment_fastq_files", tags=["alignment fastq files"])

@alignment_router.post("/")
def send_alignment_request(fastq_files: Union[str, List[str]], is_paired: bool, user_id: str, reference_file: str = None):
    
    message = {
        "fastq_files": fastq_files,
        "reference_file": reference_file,
        "is_paired": is_paired,
        "user_id": user_id
    }
    send_message(message, ALIGNMENT_FASTQ_QUEUE)

    return JSONResponse(content={"message": "Alignment operation started successfully, the result will be available soon"}, status_code=200)

