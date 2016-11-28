import sys

# for mapper code
from sqlalchemy import
Column, ForeignKey, Integer, String

# declarative_base used configuration and class code 
from sqlalchemy.ext.declarative import
declarative_base

# used in foreign key and mapper
from sqlalchemy.orm import relationship

# used in configuration
from ssqlalchemy import create_engine

# help setup class code lets sqlalch know its special classes
Base = declarative_base

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address(String(250))
    city(String(100))
    state(String(20))
    zipCode(String(15))
    website(String(250))

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    dateofbirth = Column(Date)
    gender = Column(String(6)) 
    wieght = Column(Numeric(10))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

####### insert at end of file #######

engine = create_engine('sqlite:///shelterpuppy.db')

# goes into database, adds classes as tables in db
Base.metadata.create_all(engine)