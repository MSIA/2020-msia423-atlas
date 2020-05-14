import os
from os import path

# If True, then the data will be written to an RDS instance based on your configurations
# IF False, then the data will be written to a local SQLite database based on your configurations
RDS_FLAG = False

# If RDS_FLAG is False, you need to specify a write path for the local SQLite DB
LOCAL_DB_WRITE_PATH = path.dirname(path.abspath(__file__))+'/data/sqlite_dog_breeds.db'

S3_BUCKET_NAME = 'nu-jakeatlas-s3'
RAW_DATA_FILENAME = "raw_data.csv"
RAW_DATA_WRITE_LOCATION = "./data/external/" + RAW_DATA_FILENAME
RAW_DATA_PATH = './data/external/raw_data.csv'
S3_PUBLIC_KEY = 'AKIAJUNUGIQUCKQYHMWQ'
MSIA423_S3_SECRET = os.environ.get('MSIA423_S3_SECRET')
