# Dog Breed Recommender Web App
Jake Atlas, with QA contributions from Brian Cai

Northwestern University MS in Analytics Course Project: Analytics Value Chain

## Setting Up
1) Navigate to the root of the repository. 
```bash
vi config.py 
```
You can select whether you'd like to use an RDS instance or a local SQLite database by changing the RDS_FLAG variable. Setting it to True will put the data in your RDS instance, whereas setting it to False will put the data in a local SQLite database at the path specified in LOCAL_DB_WRITE_PATH. Please note that if you would like the app to run quickly, it is recommended to set it to False and create a local DB. The loading time on the web app is on the order of 10 seconds when using an RDS instance but only about 2 seconds if you use a local SQLite DB.

Only make changes to the other variables if you are moving or renaming the data. It is highly recommended to not move or rename the data. The data currently lives in `/2020-msia423-atlas/data/raw_data.csv`. If you choose to make changes here, you may have to debug the code.

2) Add your secret key, public key, and bucket name for S3 to your environment variables. Also specify the database name to be `msia423_db`:
```bash
export MSIA423_S3_SECRET=<insert your S3 secret key here and remove carat brackets>
export S3_PUBLIC_KEY=<insert your S3 public key here and remove carat brackets>
export S3_BUCKET_NAME=<insert your S3 bucket name here and remove carat brackets>
export DATABASE_NAME=msia423_db
```

3) Make sure your IP address matches with your RDS settings. If using my RDS instance, you'll need to be on the Northwestern University VPN.

4) Edit the .mysqlconfig file to match your credentials. From the root of the repository run:
```bash
vi .mysqlconfig
```

* Set `MYSQL_USER` to the "master username" that you used to create the database server (default is 'admin' when setting up RDS instance).
* Set `MYSQL_PASSWORD` to the "master password" that you used to create the database server.
* Set `MYSQL_HOST` to be the RDS instance endpoint from the console
* Set `MYSQL_PORT` to be `3306` (or whatever your port is)

Now set the environment variables in your `~/.bashrc`

```bash
echo 'source .mysqlconfig' >> ~/.bashrc
source ~/.bashrc
```

4) Open the `your_dog_characteristic_preferences.xlsx` file in the root of the repository and provide your information in the `Your Preference` column. Since you may want to run the recommender multiple times but your preferences will remain unchanged, this section has been left as an Excel file instead of being included in the user interface of the web app. This way, you will not have to put all of the information in a second time in order to regenerate recommendations.

## Running the App
5) Build the Docker image and run the container to populate the database and get the app up and running
```bash
docker build -f app/Dockerfile -t dogbreed .
sh run_docker.sh
```

The app is now running at `http://0.0.0.0:5000/`! Please enter this URL in a web browser and find out what dog breeds are best for you! Also, as a part of this process, your data is now in the database, with the schema defined, and the raw data has also been added to your S3 bucket. If you've used an RDS instance, you can choose to explore the data (this is not necessary) by using the MySQL client. If you'd like to skip this (recommended for just running the app), please skip to step 6 below. Otherwise, run the `run_mysql_client.sh` script that allows connection to your SQL database:

```bash
sh run_mysql_client.sh
```

You can query the dog_breeds table in the msia423_db database as follows:

```bash
use msia423_db;
```
Now enter queries. For example, if you want to see all dogs that have "Retriever" in their breed name, try:
```bash
SELECT breedname FROM dog_breeds WHERE breedname LIKE '%%Retriever%%';
```
The expected output of that query is:
```bash
+------------------------------------------------+
| breedname                                        |
+------------------------------------------------+
| Chesapeake Bay Retriever               |
| Curly-Coated Retriever                     |
| Flat-Coated Retriever                       |
| Golden Retriever                              |
| Labrador Retriever                           |
| Nova Scotia Duck Tolling Retriever  |
+-----------------------------------------------+
```

To exit the system, just type:
```bash
exit;
```

6) To stop the Docker container, open a new terminal window and type the following commands:
```bash
docker kill dog_breed_recommender
docker rm dog_breed_recommender
```

At this point the app and Docker container are no longer running. Congratulations on taking the first step in researching your new dog!

## Testing
There are times that the app will struggle to give you a number of dogs near what you've asked for, particularly depending on your specifications. To provide you with advance knowledge of whether your recommendations are likely to differ significantly from the requested number, you can fill out the `your_dog_breed_characteristic_preferences.xlsx` sheet and then navigate to the `testing` directory of the repository (make sure you've followed the steps in `Setting Up` first). There, test:
```bash
python3 testing.py
```
If the tests fail, the app will not break, but when you request to see some number of dogs, you may get a wildly different number than you'd hoped. 
