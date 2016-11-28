from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# This is how you enter a new entry
# newEntry = ClassName(property="value",...)
# session.add(newEntry)
# session.commit()

def getAllRestaurants():
    """Function to return a list of all restaurants"""
    restaurantlist = session.query(Restaurant).all()
    return restaurantlist

def addNewRestaurant(name):
    """Function to add a new restaurant to the DB

    Args:
      name: the restaurant name (need not be unique).
    """
    newRestuarnt = Restaurant(name = name)
    session.add(newRestuarnt)
    session.commit()
    return

def getRestaurantName(r_id):
    myRestaurantName = session.query(Restaurant).filter_by(id =
                       r_id).one()
    return myRestaurantName.name

def editRestaurant(r_id,name):
    """Function to add a new restaurant to the DB
    
    Args:
      r_id: the id of the restaurant to be queried
      name: the edited restaurant name (need not be unique).
      """
    editRestaurant = session.query(Restaurant).filter_by(id = r_id).one()
    editRestaurant.name = name
    session.add(editRestaurant)
    session.commit()
    return

def deleteRestaurant(r_id):
    myRestaurant = session.query(Restaurant).filter_by(id = r_id).one()
    session.delete(myRestaurant)
    session.commit()
    return