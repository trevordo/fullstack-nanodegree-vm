from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore',
 r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
 "and SQLAlchemy must convert from floating point - rounding errors and other "
 "issues may occur\. Please consider storing Decimal numbers as strings or "
 "integers on this platform for lossless storage\.$",
 SAWarning, r'^sqlalchemy\.sql\.type_api$')

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Using SQLAlchemy perform the following queries on your database:
# 1. Query all of the puppies and return the results in ascending alphabetical order
allpuppies = session.query(Puppy).order_by(Puppy.name).all()

for pup in allpuppies:
	print pup.name
	print pup.shelter.name
	print '\n'

# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
# youngins = session.query(Puppy).\
#		   filter((Puppy.dateOfBirth -
#		   datetime.datetime.utcnow()) >
#	       datetime.timedelta(weeks=24)).all()
min_months = datetime.datetime.now()-datetime.timedelta(weeks=24)

youngins = session.query(Puppy).\
		  filter(Puppy.dateOfBirth > min_months).\
		  order_by(Puppy.dateOfBirth.desc()).all()

for pup in youngins:
	print pup.name
	print pup.dateOfBirth
	print '\n'


# 3. Query all puppies by ascending weight
fat = session.query(Puppy).\
	  order_by(Puppy.weight.desc()).all()

for pup in fat:
	print pup.name
	print pup.weight
	print '\n'


# 4. Query all puppies grouped by the shelter in which they are staying
shelter = session.query(Puppy).\
		  order_by(Puppy.shelter_id).all()

for pup in shelter:
	print pup.name
	print pup.shelter.name
	print '\n'
