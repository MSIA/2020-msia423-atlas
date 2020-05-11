import boto3
import config
from dog_breeds_db import establish_schema_RDS

#%% READ THE DATA FROM S3
# s3 = boto3.resource('s3')
# bucket = s3.Bucket(config.S3_BUCKET_NAME)
# bucket.download_file(config.RAW_DATA_FILENAME, config.RAW_DATA_WRITE_LOCATION)

#%% WRITE THE DATA TO S3 
s3 = boto3.client('s3', aws_access_key_id=config.S3_PUBLIC_KEY, aws_secret_access_key=config.MSIA423_S3_SECRET)
s3.upload_file(config.RAW_DATA_PATH, config.S3_BUCKET_NAME, config.RAW_DATA_FILENAME)

# Set up RDS
establish_schema_RDS()