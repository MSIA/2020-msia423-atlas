#!/usr/bin/env bash

if [ -z "$SQLALCHEMY_DATABASE_URI" ]
then
        echo "BEGINNING SETUP"
        python3 src/store_data_s3.py
fi

python3 app.py