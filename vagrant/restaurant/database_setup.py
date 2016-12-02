import sys

# for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# declarative_base used configuration and class code 
from sqlalchemy.ext.declarative import declarative_base

# used in foreign key and mapper
from sqlalchemy.orm import relationship

# used in configuration
from sqlalchemy import create_engine

# help setup class code lets sqlalch know its special classes
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250)) 
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

####### insert at end of file #######

engine = create_engine('sqlite:///restaurantmenu.db')

# goes into database, adds classes as tables in db
Base.metadata.create_all(engine)