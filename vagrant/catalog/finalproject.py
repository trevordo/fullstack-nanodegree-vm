import controller
import json

from datetime import datetime, date
from database import Department, Base, Seminar, User
from flask import Flask, render_template, request, redirect, url_for, \
                  flash, jsonify, make_response

from routes import *


# create instance of class with name of running application as arg
# anytime we run an application in python a special variable called
# name gets defined for the application an all of imports it uses
app = Flask(__name__)

app.register_blueprint(routes)


# User Helper Functions

def createUser(login_session):
    user = controller.createUser(login_session)
    return user.id

def getUserInfo(user_id):
    user = getUserInfo(user_id)
    return user

def getUserID(email):
    try:
        user = controller.getUserID(email)
        return user.id
    except:
        return None



# Making an API Endpoint (GET Request) for JSON
@app.route('/Department/<int:department_id>/seminar/JSON')
def departmentSeminarJSON(department_id):
    listOfSeminars = controller.getAllSeminarItems(department_id)   
    return jsonify(Seminars=[i.serialize for i in listOfSeminars])

@app.route('/Department/JSON')
def departmentJSON():
    listOfDeparments = controller.getAllDepartments()
    return jsonify(Departments=[i.serialize for i in listOfDeparments])


# the application run by the python interpreter gets a name variable
# set to __main__ where all other imported python files gets __name__
# variable set to actual name of python file
# if statement here makes sure the server runs only if the script is executed
# directly from the python interpreter and not used as an imported module
# if imported dont do if statement but access to rest of the code available
if __name__ == '__main__':
    app.secret_key = "Super_Secret_Key"
    # helpful debugger so webserver doesnt need to be restarted
    app.debug = True
    # run function to run local server 
    app.run(host='0.0.0.0', port=5000)