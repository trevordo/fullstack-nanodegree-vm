from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from database import Department, Base, Seminar, User

engine = create_engine('sqlite:///departmentalseminar.db')
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

# Department functions
def getAllDepartments():
    """Function to return a list of all Department"""
    departmentList = session.query(Department).all()
    return departmentList

def getDepartment(d_id):
    myDepartment = session.query(Department).filter_by(id = d_id).one()
    return myDepartment

def getDepartmentUser(d_id):
    myDepartmentUser = session.query(Department).filter_by(id = d_id).one()
    return myDepartmentUser.user_id

def addNewDepartment(name, description, user_id):
    """Function to add a new Department to the DB

    Args:
      name: the Department name (need not be unique).
    """
    newDepartment = Department(name = name, 
                               description=description, 
                               user_id=user_id)
    session.add(newDepartment)
    session.commit()
    return

def editDepartment(d_id,name,description):
    """Function to add a new Department to the DB
    
    Args:
      d_id: the id of the Department to be queried
      name: the edited Department name (need not be unique).
      description: the description of the Department
    """
    editDepartment = session.query(Department).filter_by(id = d_id).one()
    editDepartment.name = name
    editDepartment.description = description
    session.add(editDepartment)
    session.commit()
    return

def deleteDepartment(d_id):
    """Function to delete a Department from the DB
    
    Args:
      d_id: the id of the Department to be queried
    """
    myDepartment = session.query(Department).filter_by(id = d_id).one()
    session.delete(myDepartment)
    session.commit()
    return

# Menu Items functions
def getAllSeminarItems(d_id):
    """Function to retrieve all the seminars from the DB
    
    Args:
      d_id: the id of the Department to be queried in which the relationship 
            is tied too
    """
    items = session.query(Seminar).filter_by(department_id = d_id).all()
    return items

def getSeminarItem(s_id):
    getSeminar = session.query(Seminar).filter_by(id = s_id).one()
    return getSeminar

def getSeminarItemUser(s_id):
    getSeminar = session.query(Seminar).filter_by(id = s_id).one()
    return getSeminar.user_id

def addNewSeminar(t,s,a,d,b,r,u,department):
    """Function to add a new Seminar
    Args:
      r: the id of the Department to be queried
      s: the title of the seminar parameter
      a: the abstract parameter
      d: the date parameter
      b: the building parameter
      r: the room parameter
      s_id: the seminar id
      
    Use *args in parameter 
    def test_var_args_call(arg1, arg2, arg3):
    print "arg1:", arg1
    print "arg2:", arg2
    print "arg3:", arg3

    args = ("two", 3)
    test_var_args_call(1, *args)
    """
    newSeminar = Seminar(title=t,
                         speaker=s,
                         abstract=a,
                         date_time=d,
                         building=b,
                         room=r,
                         user_id=u,
                         department=department)
    print newSeminar
    session.add(newSeminar)
    session.commit()
    return

def editSeminar(t,s,a,d,b,r,s_id):
    """Function to edit a seminar in the DB
    
    Args:
      r: the id of the Department to be queried
      s: the title of the seminar parameter
      a: the abstract parameter
      d: the date parameter
      b: the building parameter
      r: the room parameter
      s_id: the seminar id
    """
    editSeminar = session.query(Seminar).filter_by(id = s_id).one()
    editSeminar.title = t
    editSeminar.speaker = s
    editSeminar.abstract = a
    editSeminar.date_time = d
    editSeminar.building = b
    editSeminar.room = r
    session.add(editSeminar)
    session.commit()
    return

def deleteSeminar(s_id):
    """Function to delete a seminar from the DB
    
    Args:
      s_id: the id of the seminar to be queried
    """
    getSeminar = session.query(Seminar).filter_by(id = s_id).one()
    session.delete(getSeminar)
    session.commit()
    return

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user
    except:
        return None