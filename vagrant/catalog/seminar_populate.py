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

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com")
session.add(User1)
session.commit()

User2 = User(name="Trevor Do", email="trevordo@gmail.com")
session.add(User2)
session.commit()


# Departments and Seminars
department1 = Department(user_id=1,
                         name="Medical Biophysics", 
                         description="""Medical physics (also called biomedical 
                         physics, medical biophysics or applied physics in 
                         medicine) is, generally speaking, the application of 
                         physics concepts, theories and methods to medicine or 
                         healthcare. Medical physics departments may be found 
                         in hospitals or universities.""")

session.add(department1)
session.commit()

seminar1 = Seminar(user_id=1,
                   title="Seminar course basics: the what and the how", 
                   speaker="Dr. Alex Vitkin",
                   abstract="Introduction seminar",
                   date_time=date(2016, 9, 28),
                   building="Princess Margaret",
                   room="Auditorium",
                   department=department1)

session.add(seminar1)
session.commit()


seminar2 = Seminar(user_id=2,
                   title="How to give a scientific talk", 
                   speaker="Dr. John Rubinstein",
                   abstract="Practical seminar",
                   date_time=date(2016, 9, 28),
                   building="Princess Margaret",
                   room="Auditorium",
                   department=department1)

session.add(seminar2)
session.commit()

# Second department and seminar
department1 = Department(user_id=1,
                         name="Medical Oncology", 
                         description="""Oncology is a branch of medicine that 
                         deals with the prevention, diagnosis and treatment of 
                         cancer. A medical professional who practices oncology 
                         is an oncologist. The name's etymological origin is 
                         the Greek word onkos, meaning "tumor", 
                         "volume" or "mass".""")

session.add(department1)
session.commit()


seminar1 = Seminar(user_id=1,
                   title="Sollazzo, Peter", 
                   speaker="Targeting differentiation pathways in Neuroblastoma",
                   abstract="Neuroblastoma (NB) is a type of cancer that forms in certain types of nerve tissue",
                   date_time=date(2016, 10, 11),
                   building="Sunnybrook",
                   room="Theatre",
                   department=department1)

session.add(seminar1)
session.commit()

# Menu for Panda Garden
department1 = Department(user_id=2,
                         name="Pathology", 
                         description="""Pathology (from the Greek roots of 
                         pathos, meaning "experience" or "suffering", 
                         and -logia, "study of") is a significant 
                         component of the causal study of disease and a major 
                         field in modern medicine and diagnosis.""")

session.add(department1)
session.commit()


seminar1 = Seminar(user_id=2,
                   title="The Big Data Rush: An Introduction to Data Science", 
                   speaker="Geraghty, Benjamin",
                   abstract="The next big thing",
                   date_time=date(2016, 10, 18),
                   building="Sunnybrook",
                   room="Theatre",
                   department=department1)

session.add(seminar1)
session.commit()

seminar2 = Seminar(user_id=2,
                   title="Monoclonal antibodies specifically targeting amyloidogenic forms of transthyretin (TTR) with potential to treat TTR-related cardiomyopathy and polyneuropathy", 
                   speaker="Galant, Natalie",
                   abstract="Targeting heart and neuro diseases with mabs",
                   date_time=date(2016, 10, 25),
                   building="Princess Margaret",
                   room="Auditorium",
                   department=department1)

session.add(seminar2)
session.commit()

seminar3 = Seminar(user_id=2,
                   title="Identification of Prognostic Gene Signatures in Hepatocellular Carcinoma", 
                   speaker="Bhat, Mamatha",
                   abstract="Genetics and liver tumors",
                   date_time=date(2016, 10, 26),
                   building="TMDT",
                   room="4-201",
                   department=department1)

session.add(seminar3)
session.commit()



print "added items!"