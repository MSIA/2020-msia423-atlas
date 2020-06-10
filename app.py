import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from src.recommend_dogs import recommend_dogs
from src.store_data_s3 import read_from_s3
from flask import Flask
import pandas as pd
import os

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

@app.route('/')
def index():
    """Main view that lists dog breeds in the database.

    Create view into index page that collects user input data.

    Returns: rendered html template

    """

    try:
        logger.debug("Index page accessed")
        try:
            recommendations = list(pd.read_csv('./app/.recommended_breeds.csv')['Your Recommended Dog Breeds'])
        except Exception as e:
            # .recommended_breeds.csv was deleted or moved: recreate
            logger.debug(e)
            recommendations = []
        pd.DataFrame(columns=['Your Recommended Dog Breeds']).to_csv('./app/.recommended_breeds.csv')
        if len(recommendations) > 0:
            return render_template('index.html', recommendations=recommendations)
        else:
            return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display breed recommendations, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with input of approximate number of dog breeds to get

    :return: redirect to index page
    """

    try:
        num_dogs = request.form['numdogs']
        logger.debug('The number of dogs is: '+ num_dogs)
        recommendations = recommend_dogs(int(num_dogs))
        try:
            pd.DataFrame(recommendations, columns=['Your Recommended Dog Breeds']).to_csv('./app/.recommended_breeds.csv')
        except Exception as e:
            logger.debug(e)
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display breed recommendations, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    # Download the data from S3
    if os.environ.get("AWS_SECRET_ACCESS_KEY") is not None:
        read_from_s3() 
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])