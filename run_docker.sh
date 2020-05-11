docker run -it \
--env MYSQL_HOST \
--env MYSQL_PORT \
--env MYSQL_USER \
--env MYSQL_PASSWORD \
--env DATABASE_NAME \
--env MSIA423_S3_SECRET \
dog_breeds_mysql store_data_s3.py