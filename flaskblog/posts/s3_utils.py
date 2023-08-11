import boto3
import uuid
from flask import app

def upload_to_s3(file, file_name):
    s3 = boto3.client('s3', aws_access_key_id=app.config['AWS_ACCESS_KEY'],
                      aws_secret_access_key=app.config['AWS_SECRET_KEY'])
    
    bucket_name = app.config['S3_BUCKET_NAME']
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)

    file = File(original_filename=uploaded_file.filename, filename=new_filename,
                bucket=bucket_name, region="us-east-2")
    return file_url

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'mov', 'mp4', 'avi', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  