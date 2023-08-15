import boto3
import botocore
import os
import uuid
from flask import app

def upload_to_s3(file, acl="public-read"):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    S3_LOCATION = os.environ.get('S3_LOCATION')

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        return {"errors": str(e)}

    return f"{S3_LOCATION}{file.filename}"

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'mov', 'mp4', 'avi', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  