# ─────────────────────────────────────────────────────
# All S3/MinIO operations live here.
# Views never import boto3 directly.
# Same pattern as cloudinary_service.py and email_service.py
# ─────────────────────────────────────────────────────

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import os


def get_s3_client():
    """
    Connection to S3/MinIO) 
    Creates client object with credentials
    This function returns a connection object, not data

    endpoint_url=None → real AWS S3
    endpoint_url=http://localhost:9000 → MinIO local
     
    """
    return boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


# ── UPLOAD FILE ──────────────────────────────────────
# Standard upload — backend receives file, uploads to S3.
# Use for: server-side generated files (PDFs, reports)
# Avoid for: user uploads (use direct upload instead)
# ─────────────────────────────────────────────────────
def upload_file(file_obj, object_name: str, content_type: str = None) -> str:
    """
    Upload a file to S3/MinIO.

    file_obj    → file-like object or bytes
    object_name → path in bucket e.g. 'receipts/2026/receipt-123.pdf'
    Returns:    → public URL of uploaded file
    """
    client = get_s3_client()

    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type

    client.upload_fileobj(
        file_obj,
        settings.AWS_STORAGE_BUCKET_NAME,
        object_name,
        ExtraArgs=extra_args
    )

    return f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{object_name}"


# ── DELETE FILE ──────────────────────────────────────
def delete_file(object_name: str) -> bool:
    """
    Delete a file from S3/MinIO.
    object_name → same path used during upload
    """
    client = get_s3_client()

    try:
        client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=object_name
        )
        return True
    except ClientError as e:
        print(f"Delete failed: {e}")
        return False


# ── PRE-SIGNED URL (UPLOAD) ──────────────────────────
# This is the key pattern for direct uploads.
#
# WHAT IS A PRE-SIGNED URL?
# A temporary URL that gives ONE person permission
# to upload ONE specific file directly to S3/MinIO
# without going through your server.
#
# FLOW:
# 1. Frontend asks your backend: "I want to upload profile.jpg"
# 2. Your backend generates a pre-signed URL (expires in 5 mins)
# 3. Backend returns URL to frontend
# 4. Frontend uploads DIRECTLY to S3 using that URL
# 5. Your server never touches the file bytes
#
# WHY THIS MATTERS:
# → 100MB video upload doesn't block your Django process
# → Your server bandwidth not consumed
# → S3 handles the upload scaling
# ─────────────────────────────────────────────────────
def generate_presigned_upload_url(
    object_name: str,
    content_type: str,
    expiry: int = 300  # 5 minutes
) -> dict:
    """
    Generate a pre-signed URL for direct frontend → S3 upload.

    object_name  → where file will be stored e.g. 'uploads/user_12/cv.pdf'
    content_type → must match what frontend actually uploads
    expiry       → seconds until URL expires (default 5 min)

    Returns dict with url and fields frontend needs to POST
    """
    client = get_s3_client()

    response = client.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=object_name,
        Fields={
            'Content-Type': content_type,
        },
        Conditions=[
            {'Content-Type': content_type},
            ['content-length-range', 1, 10 * 1024 * 1024],  # 1 byte to 10MB
        ],
        ExpiresIn=expiry
    )

    # response = {
    #   'url': 'http://localhost:9000/yourapp-media',
    #   'fields': {
    #     'key': 'uploads/user_12/cv.pdf',
    #     'Content-Type': 'application/pdf',
    #     'policy': 'base64encodedpolicy...',
    #     'x-amz-signature': 'signature...',
    #   }
    # }
    # Frontend POSTs multipart form with these fields + the file

    return response


# ── PRE-SIGNED URL (DOWNLOAD) ────────────────────────
# Temporary secure access to PRIVATE files.
#
# USE CASE:
# Loan contract PDF — only the member who borrowed
# should be able to download it. Not public.
#
# Generate a URL that expires in 1 hour.
# After 1 hour → link is dead, file still safe in S3.
# ─────────────────────────────────────────────────────
def generate_presigned_download_url(
    object_name: str,
    expiry: int = 3600  # 1 hour
) -> str:
    """
    Generate temporary download link for private files.
    expiry → seconds until link expires (default 1 hour)
    """
    client = get_s3_client()

    url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': object_name,
        },
        ExpiresIn=expiry
    )

    return url