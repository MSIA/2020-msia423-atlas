import os
import logging
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import pandas as pd
import config

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("DATABASE_NAME")
engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

Base = declarative_base()  

class Dog(Base):
	"""Create a data model for the dtabase to be set up for capturing dog breeds """
	__tablename__ = 'dog_breeds'
	breedname = Column(String(100), primary_key=True, nullable=False)
	adaptability_apt_living = Column(Integer, unique=False, nullable=False)
	adaptability_new_owner = Column(Integer, unique=False, nullable=False)
	adaptability_sensitivity = Column(Integer, unique=False, nullable=False)
	adaptability_alone_ok = Column(Integer, unique=False, nullable=False)
	adaptability_cold_ok = Column(Integer, unique=False, nullable=False)
	adaptability_hot_ok = Column(Integer, unique=False, nullable=False)
	friendliness_family = Column(Integer, unique=False, nullable=False)
	friendliness_kids = Column(Integer, unique=False, nullable=False)
	friendliness_dogs = Column(Integer, unique=False, nullable=False)
	friendliness_strangers = Column(Integer, unique=False, nullable=False)
	health_and_grooming_shedding = Column(Integer, unique=False, nullable=False)
	health_and_grooming_drooling = Column(Integer, unique=False, nullable=False)
	health_and_grooming_grooming = Column(Integer, unique=False, nullable=False)
	health_and_grooming_health = Column(Integer, unique=False, nullable=False)
	health_and_grooming_weight_gain = Column(Integer, unique=False, nullable=False)
	health_and_grooming_size = Column(Integer, unique=False, nullable=False)
	trainability_easy = Column(Integer, unique=False, nullable=False)
	trainability_intelligence = Column(Integer, unique=False, nullable=False)
	trainability_mouthy = Column(Integer, unique=False, nullable=False)
	trainability_prey_drive	= Column(Integer, unique=False, nullable=False)
	trainability_bark = Column(Integer, unique=False, nullable=False)
	trainability_wanderlust = Column(Integer, unique=False, nullable=False)
	exercise_energy = Column(Integer, unique=False, nullable=False)
	exercise_intensity = Column(Integer, unique=False, nullable=False)	
	exercise_ex_needs = Column(Integer, unique=False, nullable=False)	
	exercise_playful = Column(Integer, unique=False, nullable=False)		
	def __repr__(self):
		return('<Dogbreed: %r>' % self.breedname)


# Set up mysql connection
engine = sql.create_engine(engine_string)

# Create the tracks table
Base.metadata.create_all(engine)

# Set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

# Create a db session
Session = sessionmaker(bind=engine)  
session = Session()

# Delete anything that's already in the table because the data is static
try:
	session.execute('''DELETE FROM dog_breeds''')
except:
	pass

# Get the data 
df = pd.read_csv(config.RAW_DATA_PATH).set_index('breed')
formatted_rows = []
for index, row in df.iterrows():
    datarow = Dog(breedname = index, 
					adaptability_apt_living = int(row.adaptability_apt_living),
					adaptability_new_owner = int(row.adaptability_new_owner),
					adaptability_sensitivity = int(row.adaptability_sensitivity),
					adaptability_alone_ok = int(row.adaptability_alone_ok),
					adaptability_cold_ok = int(row.adaptability_cold_ok),
					adaptability_hot_ok = int(row.adaptability_hot_ok),
					friendliness_family = int(row.friendliness_family),
					friendliness_kids = int(row.friendliness_kids),
					friendliness_dogs = int(row.friendliness_dogs),
					friendliness_strangers = int(row.friendliness_strangers),
					health_and_grooming_shedding = int(row.health_and_grooming_shedding),
					health_and_grooming_drooling = int(row.health_and_grooming_drooling),
					health_and_grooming_grooming = int(row.health_and_grooming_grooming),
					health_and_grooming_health = int(row.health_and_grooming_health),
					health_and_grooming_weight_gain = int(row.health_and_grooming_weight_gain),
					health_and_grooming_size = int(row.health_and_grooming_size),
					trainability_easy = int(row.trainability_easy),
					trainability_intelligence = int(row.trainability_intelligence),
					trainability_mouthy = int(row.trainability_mouthy),
					trainability_prey_drive = int(row.trainability_prey_drive),
					trainability_bark = int(row.trainability_bark),
					trainability_wanderlust = int(row.trainability_wanderlust),
					exercise_energy = int(row.exercise_energy),
					exercise_intensity = int(row.exercise_intensity),
					exercise_ex_needs = int(row.exercise_ex_needs),
					exercise_playful = int(row.exercise_playful))
    formatted_rows.append(datarow)
session.add_all(formatted_rows)
session.commit()

logger.info("Database created with all raw data added")
session.close()
