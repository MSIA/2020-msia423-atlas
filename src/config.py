import os

S3_BUCKET_NAME = 'nu-jakeatlas-s3'
RAW_DATA_FILENAME = "raw_data.csv"
RAW_DATA_WRITE_LOCATION = "./data/external/" + RAW_DATA_FILENAME
RAW_DATA_PATH = './data/external/raw_data.csv'
S3_PUBLIC_KEY = 'AKIAJUNUGIQUCKQYHMWQ'
MSIA423_S3_SECRET = os.environ.get('MSIA423_S3_SECRET')
