import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import logging
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
import src.config as config
import os
import logging

def recommend_dogs(num_dogs):
    """Queries the database and uses k-means clustering to recommend dog breeds to the user

    Args:
        num_dogs (int): An approximate number of dogs the user would like to have recommended
    
    Returns:
        final_recommendation (list of strings): The recommended dog breeds for the user
    """
    logging.debug('Attempting to make recommendations')
    random_state = 1
    if os.environ.get("SQLALCHEMY_DATABASE_URI") is None:
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        database = os.environ.get("DATABASE_NAME")
        if config.RDS_FLAG:
            engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)
        else:
            engine_string = 'sqlite:////{}'.format(config.LOCAL_DB_WRITE_PATH)
    else:
        engine_string = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # Set up mysql connection
    engine = sql.create_engine(engine_string)
    # Query the database
    logging.debug('querying the database')
    try:
        dat = pd.read_sql_table('dog_breeds', con=engine, index_col='breedname')
    except Exception as e:
        logging.debug(e)
    logging.debug(dat.head())
    logging.debug('database read')
    num_clusters = int(np.floor(np.shape(dat)[0]/num_dogs))
    recommendations = []
    for i in range(max(num_clusters-3, 2), min(num_clusters+3, 100)+1):
        km = KMeans(n_clusters=i, random_state=random_state)
        km = km.fit(dat)
        fitted_dat = dat.copy()
        fitted_dat['cluster_assignment'] = km.predict(dat)
        try:
            recommendations.append(list(fitted_dat[fitted_dat['cluster_assignment']==km.predict(np.array(list(pd.read_excel('./your_dog_characteristic_preferences.xlsx', header=2,  usecols='B:D')['Your Preference'])).reshape(1,-1))[0]].index))
        except Exception as e:
            try:
                # Will only ever work if we are in testing
                recommendations.append(list(fitted_dat[fitted_dat['cluster_assignment']==km.predict(np.array(list(pd.read_excel('./../your_dog_characteristic_preferences.xlsx', header=2,  usecols='B:D')['Your Preference'])).reshape(1,-1))[0]].index))
            except:
                logging.error('The process failed due to unallowable changes to the your_dog_characteristic_preferences file or its location: ' + str(e))
    diffs = {}
    for recommendation in recommendations:
        diff = abs(num_dogs - len(recommendation))
        diffs[diff] = recommendation
    final_recommendation = diffs.get(min(diffs))
    return(final_recommendation)