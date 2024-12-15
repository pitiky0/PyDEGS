from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import Union, List

from utils import send_message, FILTERING_FASTQ_QUEUE

filtering_router = APIRouter(prefix="/filtering_fastq_files", tags=["filtering fastq files"])

@filtering_router.post("/")
def send_quality_control_request(files: Union[str, List[str]], user_id: str, is_paired_end: bool, truncate_start_bases: int, truncate_end_bases: int,
                 left_adapter, right_adapter, min_length: int, n_bases: int, complexity: float):

    message = {
        "files": files,
        "user_id": user_id,
        "is_paired_end": is_paired_end,
        "truncate_start_bases": truncate_start_bases,
        "truncate_end_bases": truncate_end_bases,
        "left_adapter": left_adapter,
        "right_adapter": right_adapter,
        "min_length": min_length,
        "n_bases": n_bases,
        "complexity": complexity
    }
    send_message(message, FILTERING_FASTQ_QUEUE)

    return JSONResponse(content={"message": "Filtering operation started successfully, the result will be available soon"}, status_code=200)

