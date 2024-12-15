import io
import os
import json
import tempfile
import zipfile
from typing import Dict
from Bio import SeqIO
from collections import Counter
import gzip
from minio.commonconfig import CopySource
from fastapi import File, UploadFile, HTTPException, Depends, BackgroundTasks, APIRouter
from starlette.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from minio import Minio
from minio.error import S3Error
from minio.commonconfig import Tags

from minio_client import minio_client
from utils import object_exists, validate_file_format, string_value_to_list, bucket_file_handler

router = APIRouter(tags=["files-management"])


class TagRequest(BaseModel):
    tags: Dict[str, str]


async def check_bucket_exists(bucket_name: str, client: Minio):
    """Check if a bucket exists."""
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

@router.post("/{bucket_name}/upload_file/")
async def upload_file(
        bucket_name: str,
        user_id: str,
        folder_name: str = None,
        file: UploadFile = File(...),
        client: Minio = Depends(lambda: minio_client)
):
    """Uploads a file to a specified bucket in MinIO with user ID as a tag."""

    # Validate file format based on the bucket name
    validate_file_format(bucket_name, file.filename)

    # Ensure bucket exists
    await check_bucket_exists(bucket_name, client)

    if await object_exists(bucket_name, file.filename, client):
        raise HTTPException(
            status_code=400,
            detail=f"File {file.filename} already exists in bucket {bucket_name}. Try uploading another file or renaming this file."
        )

    # Read file content and get size
    file_content = await file.read()
    file_size = len(file_content)

    # Create tags with user ID
    tags = Tags(for_object=True)
    tags["uploaded_by"] = user_id

    try:
        if folder_name:
            file.filename = f"{folder_name}/{file.filename}"
        # Upload file to MinIO
        client.put_object(
            bucket_name,
            file.filename,
            io.BytesIO(file_content),
            file_size,
            content_type=file.content_type,
            tags=tags
        )
        return JSONResponse(content={"filename": file.filename, "uploaded by": user_id}, status_code=200)

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{bucket_name}/download_file/")
async def download_file(
        bucket_name: str,
        file_name: str,
        background_tasks: BackgroundTasks,
        client: Minio = Depends(lambda: minio_client)
):
    """Downloads a file from a specified bucket in MinIO."""
    await bucket_file_handler(bucket_name, file_name, client)

    try:
        # Retrieve the file from MinIO
        response = client.get_object(bucket_name, file_name)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.read())
            tmp_file_path = tmp_file.name

        response.close()
        response.release_conn()
        background_tasks.add_task(os.remove, tmp_file_path)
        return FileResponse(tmp_file_path, media_type='application/octet-stream', filename=file_name)

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{bucket_name}/download_folder/")
async def download_folder(
        bucket_name: str,
        folder_name: str,
        background_tasks: BackgroundTasks,
        client: Minio = Depends(lambda: minio_client)
):
    """Downloads all files in a specified folder in MinIO."""

    if not client.bucket_exists(bucket_name):
        raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} not found.")

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip_file:
            # Create a zip file
            with zipfile.ZipFile(tmp_zip_file, 'w') as zip_file:
                # List all objects in the bucket with the given prefix
                objects = client.list_objects(bucket_name, prefix=f"{folder_name}/", recursive=True)
                count = 0

                for obj in objects:
                    count += 1
                    print (obj.object_name)
                    if obj.is_dir:
                        continue

                    # Retrieve the file from MinIO
                    response = client.get_object(bucket_name, obj.object_name)

                    # Preserve the directory structure in the zip file
                    zip_file.writestr(obj.object_name, response.read())

                    response.close()
                    response.release_conn()
                if count == 0:
                    raise HTTPException(status_code=400, detail=f"Folder {folder_name} not exist or it is empty")
            tmp_zip_file_path = tmp_zip_file.name

        background_tasks.add_task(os.remove, tmp_zip_file_path)
        return FileResponse(tmp_zip_file_path, media_type='application/octet-stream', filename=f"{folder_name}.zip")

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{bucket_name}/get_file_info/")
async def get_file_info(
        bucket_name: str,
        file_name: str,
        client: Minio = Depends(lambda: minio_client)
):
    """Retrieves information about a file in a specified bucket in MinIO."""
    await bucket_file_handler(bucket_name, file_name, client)

    try:
        # Get the file information
        file_info = client.stat_object(bucket_name, file_name)
        file_metadata = {
            "file_name": file_info.object_name,
            "size": file_info.size,
            "last_modified": file_info.last_modified,
            "etag": file_info.etag,
            "content_type": file_info.content_type
        }

        return file_metadata

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/get_top_reads/")
async def get_top_reads(
    file_name: str,
    client: Minio = Depends(lambda: minio_client)
):
    """Retrieves top reads from a fastq file in MinIO."""
    if file_name.startswith("filtered_"):
        bucket_name = "filtered-fastq-files"
    else:
        bucket_name = "fastq-files"

    try:
        # Retrieve the file from MinIO
        response = client.get_object(bucket_name, file_name)

        read_counter = Counter()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.read())
            local_file_path = tmp_file.name
        
        response.close()
        response.release_conn()

        # Determine the file format and read the file content
        if file_name.endswith(".fastq.gz"):
            with gzip.open(local_file_path, 'rt') as file1:
                for record in SeqIO.parse(file1, "fastq"):
                    read_counter[f"{record.seq}"] += 1
        elif file_name.endswith(".fastq"):
            with open(local_file_path, 'rt') as file1:
                for record in SeqIO.parse(file1, "fastq"):
                    read_counter[f"{record.seq}"] += 1
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Clean up the local file after processing
        os.remove(local_file_path)

        obj = {"most_common": read_counter.most_common(10), "total_reads": sum(read_counter.values())}
        return JSONResponse(status_code=200, content=obj)

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
@router.get("/metadata_columns/")
async def get_metadata_columns(
    file_name: str,
    client: Minio = Depends(lambda: minio_client)
):
    """Retrieves metadata columns from a CSV or TXT file from MinIO."""

    # Retrieve the file from MinIO
    response = client.get_object("study-metadata-files", file_name)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(response.read())
        local_file_path = tmp_file.name
    
    response.close()
    response.release_conn()

    try:
        with open(local_file_path, 'r') as file:
            columns1 = file.readline().strip().split(",")
            columns2 = file.readline().strip().split("\t")
        os.remove(local_file_path)
        columns = columns1 if len(columns1) > len(columns2) else columns2
        return JSONResponse(status_code=200, content={"columns": columns})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.post("/{bucket_name}/{group_name}/group_files")
async def group_files(
    bucket_name: str,
    group_name: str,
    files: list[str],
    client: Minio = Depends(lambda: minio_client)
):
    for file in files:
        try:
            await bucket_file_handler(bucket_name, file, client)
            result = client.copy_object(bucket_name, f"{group_name}/{file}", CopySource(bucket_name, file))
            client.remove_object(bucket_name, file)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return JSONResponse(status_code=200, content={"message": f"Files successfully grouped in {group_name} folder"})

@router.post("/{bucket_name}/add_tags/")
async def add_tags(
        bucket_name: str,
        file_name: str,
        tag_request: TagRequest,
        client: Minio = Depends(lambda: minio_client)
):
    """Adds tags to a file in a specified bucket in MinIO."""
    await bucket_file_handler(bucket_name, file_name, client)

    try:
        # Get the existing tags
        old_tags = client.get_object_tags(bucket_name, file_name)

        # Merge the existing tags with the new tags
        tags = Tags(for_object=True)

        if old_tags is not None:
            tags.update(old_tags)

        for new_key, new_value in tag_request.tags.items():
            if new_key in tags:
                existing_ids = set(tags[new_key].split())
                existing_ids.add(new_value)
            else:
                existing_ids = {new_value}
            
            tags[new_key] = " ".join(existing_ids)

        # Set the updated tags
        client.set_object_tags(bucket_name, file_name, tags)
        tags = string_value_to_list(tags)
        return JSONResponse(status_code=200,
                            content={"message": f"Tags successfully added to {file_name} in bucket {bucket_name}",
                                     "tags": tags})

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{bucket_name}/get_tags/")
async def get_tags(
        bucket_name: str,
        file_name: str,
        client: Minio = Depends(lambda: minio_client)
):
    """Retrieves tags for a file in a specified bucket in MinIO."""
    file_name = file_name.rstrip("/")
    await bucket_file_handler(bucket_name, file_name, client)

    try:
        objects = client.list_objects(bucket_name, prefix=file_name)
        if any(obj.is_dir for obj in objects):
            raise HTTPException(status_code=400, detail=f"{file_name} is a folder, not a file.")
        tags = client.get_object_tags(bucket_name, file_name) or {}
        tags = string_value_to_list(tags)

        return JSONResponse(status_code=200, content={"file_name": file_name, "tags": tags})

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/{bucket_name}/list_files/")
async def list_files(
    bucket_name: str,
    client: Minio = Depends(lambda: minio_client)
):
    """Lists all files in a specified bucket in MinIO."""

    if not client.bucket_exists(bucket_name):
        raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} not found.")

    try:
        objects = client.list_objects(bucket_name, recursive=True)
        file_list = []

        for obj in objects:
            # Skip directories
            if obj.is_dir:
                continue

            # Get file information
            file_info = {
                "file_name": obj.object_name,
                "tags": {}
            }

            try:
                tags = client.get_object_tags(bucket_name, obj.object_name)
                file_info["tags"] = tags if tags else {}
            except S3Error as e:
                file_info["tags"] = {"error": str(e)}

            file_list.append(file_info)

        return {"bucket": bucket_name, "files": file_list}

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.delete("/{bucket_name}/delete_file/")
async def delete_file(
        bucket_name: str,
        file_name: str,
        client: Minio = Depends(lambda: minio_client)
):
    """Deletes a file from a specified bucket in MinIO."""
    await bucket_file_handler(bucket_name, file_name, client)

    try:
        objects = client.list_objects(bucket_name)
        for obj in objects:
            if obj.object_name in [file_name, f"{file_name}/"] and obj.is_dir:
                raise HTTPException(status_code=400, detail=f"{file_name} is a folder, not a file.")

        # Delete the file from MinIO
        client.remove_object(bucket_name, file_name)
        return JSONResponse(status_code=200,
                            content={"message": f"File {file_name} successfully deleted from bucket {bucket_name}"})

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
