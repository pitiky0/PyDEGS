import requests
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from utils import FILES_MANAGEMENT_SERVICE

files_router = APIRouter(prefix="/files", tags=["files-management"])

@files_router.get("/{bucket_name}/get_file_info/")
async def get_file_info(bucket_name: str, file_name: str):
    response = requests.get(f"{FILES_MANAGEMENT_SERVICE}/{bucket_name}/get_file_info/",
                            params={"file_name": file_name})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@files_router.post("/{bucket_name}/add_tags/")
async def add_tags(bucket_name: str, file_name: str, request: Request):
    tag_data = await request.json()
    response = requests.post(f"{FILES_MANAGEMENT_SERVICE}/{bucket_name}/add_tags/",
                             json=tag_data, params={"file_name": file_name})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@files_router.get("/{bucket_name}/get_tags/")
async def get_tags(bucket_name: str, file_name: str):
    response = requests.get(f"{FILES_MANAGEMENT_SERVICE}/{bucket_name}/get_tags/",
                            params={"file_name": file_name})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@files_router.get("/{bucket_name}/list_files/")
async def list_files(bucket_name: str):
    response = requests.get(f"{FILES_MANAGEMENT_SERVICE}/{bucket_name}/list_files/")
    return JSONResponse(content=response.json(), status_code=response.status_code)

@files_router.delete("/{bucket_name}/delete_file/")
async def delete_file(bucket_name: str, file_name: str):
    response = requests.delete(f"{FILES_MANAGEMENT_SERVICE}/{bucket_name}/delete_file/",
                               params={"file_name": file_name})
    return JSONResponse(content=response.json(), status_code=response.status_code)

@files_router.get("/get_top_reads/")
async def get_top_reads(file_name: str):
    response = requests.get(f"{FILES_MANAGEMENT_SERVICE}/get_top_reads/?file_name={file_name}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

@files_router.get("/get_metadata_columns/")
async def get_metadata_columns(file_name: str):
    response = requests.get(f"{FILES_MANAGEMENT_SERVICE}/metadata_columns/?file_name={file_name}")
    return JSONResponse(content=response.json(), status_code=response.status_code)