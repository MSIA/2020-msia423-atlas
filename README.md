# MSiA 423 Project Repository

## Midpoint
### Getting the data into S3
Navigate to `/2020-msia423-atlas/src/config.py`.
1. Fill in your information for S3_BUCKET_NAME and S3_PUBLIC_KEY. Only make changes to the other variables if you are moving or renaming the data. It is highly recommended to not move or rename the data. The data currently lives in `/2020-msia423-atlas/data/raw_data.xlsx`.

2) Add your secret key for S3 to your environment variables:
```bash
export MSIA423_S3_SECRET=<insert your secret key here and remove carat brackets>
```

3) Run the store_data_s3.py file
```bash
python ./src/store_data_s3.py
```

The raw data is now in your S3 bucket! 

### Setting up your database with RDS
1) Make sure your IP address matches with your RDS settings
2) Edit the mysql config file to match your credentials. From the root of the repository run:
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

3) Verify that your MySQL client is functional. Run the `run_mysql_client.sh` script that creates a Docker container with a connection to your SQL database.

```bash
sh run_mysql_client.sh
```

If you are going through these instructions for the first time, skip from here to step 4. However, once you've completed the process, you can later return to this step and run queries. Once you've completed these steps, you can query the dog_breeds table in the msia423_db database as follows:

```bash
use msia423_db;
```
Now enter queries. For example, if you want to see all dogs that have "Retriever" in their breed name, try:
```bash
SELECT breedname FROM dob_breeds WHERE breedname LIKE '%%Retriever%%';
```
To exit the system, just type:
```bash
exit;
```

4) Build the Docker image
```bash
docker build -t dog_breeds_mysql .
```

5) Set your database name and run the Docker container
```bash
export DATABASE_NAME=msia423_db
sh run_docker.sh
```

Your data is now in the database! Feel free to return to step 3 to verify that the data looks as expected:
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


# Template Stuff

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
