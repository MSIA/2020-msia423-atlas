import boto3
import config
from dog_breeds_db import establish_schema

def read_from_s3():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config.S3_BUCKET_NAME)
    bucket.download_file(config.RAW_DATA_FILENAME, config.RAW_DATA_WRITE_LOCATION)

def write_to_s3():
    s3 = boto3.client('s3', aws_access_key_id=config.S3_PUBLIC_KEY, aws_secret_access_key=config.MSIA423_S3_SECRET)
    s3.upload_file(config.RAW_DATA_PATH, config.S3_BUCKET_NAME, config.RAW_DATA_FILENAME)

# Set up RDS
if __name__=="__main__":
    write_to_s3()
    establish_schema()