docker run -it \
-p 5000:5000 \
--env MYSQL_HOST \
--env MYSQL_PORT \
--env MYSQL_USER \
--env MYSQL_PASSWORD \
--env DATABASE_NAME \
--env MSIA423_S3_SECRET \
--mount type=bind,source="$(pwd)",target=/app/ \
--name dog_breed_recommender dogbreed