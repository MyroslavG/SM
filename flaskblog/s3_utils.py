import boto3
import uuid
from flask import app, current_app

def upload_to_s3(uploaded_file, file_name):
    s3 = boto3.client('s3', aws_access_key_id='',
                      aws_secret_access_key='')

    #current_app.config['AWS_ACCESS_KEY']                  
    #current_app.config['AWS_SECRET_KEY']

    bucket_name = 'povodyrcom' #current_app.config['S3_BUCKET_NAME']
    #s3 = boto3.resource("s3")

    try:
        s3.upload_file(
            uploaded_file,
            bucket_name,
            uploaded_file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": uploaded_file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    #s3.Bucket(bucket_name).upload_fileobj(uploaded_file, file_name)

    #file = File(original_filename=uploaded_file.filename, filename=file_name,
    #            bucket=bucket_name, region="us-east-2")
    return 'https://povodyrcom.s3.amazonaws.com/' + file_name

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'mov', 'mp4', 'avi', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  