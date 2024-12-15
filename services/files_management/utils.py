from fastapi import HTTPException
from minio import Minio, S3Error
from typing import Dict

# Define the buckets and allowed file formats
BUCKET_FILE_FORMATS = {
    "fastq-files": [".fastq.gz", ".fastq", ".fq.gz", ".fq", ".fasta.gz", ".fa", ".fasta"],
    "quality-control-files": [".html", ".zip"],
    "filtered-fastq-files": [".fastq.gz", ".fastq", ".fq.gz", ".fq", ".fasta.gz", ".fa", ".fasta", ".txt"],
    "reference-genomes-files": [".fa", ".fna", ".fna.gz", ".fa.gz"],
    "alignment-files": [".bam", ".sam", ".log"],
    "gtf-gff-files": [".gff.gz", ".gtf.gz", ".gff3.gz", ".gff", ".gtf", ".gff3"],
    "quantification-files": [".csv", ".txt"],
    "study-metadata-files": [".csv", ".txt"],
    "def-expression-files": [".csv", ".png", ".txt"]
}

async def bucket_exists(bucket_name: str, client: Minio) -> bool:
    try:
        return client.bucket_exists(bucket_name)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Error checking bucket: {e}")

async def object_exists(bucket_name: str, object_name: str, client: Minio) -> bool:
    try:
        objects = client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            if obj.object_name == object_name or obj.object_name == f"{object_name}/":
                return True
        return False
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Error listing objects: {e}")

def validate_file_format(bucket_name: str, file_name: str):
    allowed_formats = BUCKET_FILE_FORMATS.get(bucket_name)
    if allowed_formats is None:
        raise HTTPException(status_code=400, detail=f"Invalid bucket name: {bucket_name}")

    if not any(file_name.endswith(ext) for ext in allowed_formats):
        raise HTTPException(status_code=400, detail=f"Unsupported file format for bucket {bucket_name}: {file_name} allowed formats: {allowed_formats}")

def string_value_to_list(tags: Dict[str, str]) -> Dict[str, list]:
    if tags is not None:
        return {key: value.split() if isinstance(value, str) and " " in value else value for key, value in tags.items()}
    return {}

async def bucket_file_handler(bucket_name: str, file_name: str, client: Minio):
    if bucket_name not in BUCKET_FILE_FORMATS:
        raise HTTPException(status_code=400, detail=f"Invalid bucket name: {bucket_name}")

    if not await bucket_exists(bucket_name, client):
        raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} does not exist.")

    if not await object_exists(bucket_name, file_name, client):
        raise HTTPException(status_code=404, detail=f"File {file_name} does not exist in bucket {bucket_name} or it is a directory.")
