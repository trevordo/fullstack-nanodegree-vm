import controller

from datetime import datetime, date
from database import Department, Base, Seminar
from flask import Flask, render_template, request, redirect, url_for, \
                  flash, jsonify, make_response
# These import are for anti-forgery state token creation 
from flask import session as login_session
import random, string
# These imports are for Gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Seminar App"

# create instance of class with name of running application as arg
# anytime we run an application in python a special variable called
# name gets defined for the application an all of imports it uses
app = Flask(__name__)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# decorator wraps function into app.route function if any of these
# addresses get entered, the HelloWorld function gets executed
@app.route('/')
@app.route('/Department')
def departmentList():
    listOfDeparments = controller.getAllDepartments()
    return render_template('department.html', departments=listOfDeparments)


@app.route('/Deparment/<int:department_id>/')
def departmentSeminars(department_id):
    # From controller get a list of all items
    getdepartment = controller.getDepartment(department_id)
    listOfSeminars = controller.getAllSeminarItems(department_id)
    # render template
    return render_template('seminars.html', 
                            department=getdepartment, 
                            items=listOfSeminars)

@app.route('/Deparment/new/', methods=['GET','POST'])
def newDepartment():
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method =='POST':
        if request.form['name'] and request.form['description']:
            editName = request.form['name']
            editDesc = request.form['description']
            # Add department to controller
            controller.addNewDepartment(editName,editDesc)
            flash("Department Added Successfully!")
        return redirect(url_for('departmentList'))
    else:
        return render_template('newdepartment.html')
            
    return "page to add Deparment"

@app.route('/Deparment/<int:department_id>/edit/', methods=['GET','POST'])
def editDepartment(department_id):
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method =='POST':
        if request.form['name']:
            editName = request.form['name']
            dept = controller.getDepartment(department_id)
            editDesc = dept.description
            # check for empty description field
            if request.form['description']:
                editDesc = request.form['description']
            # Edit department to controller
            controller.editDepartment(department_id,editName,editDesc)
            flash("Department Edited Successfully!")
        return redirect(url_for('departmentList'))
    else:
        getdepartment = controller.getDepartment(department_id)
        return render_template('editdepartment.html', department=getdepartment)

@app.route('/Deparment/<int:department_id>/delete/', methods=['GET','POST'])
def deleteDepartment(department_id):
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method =='POST':
        # Delete department to controller
        controller.deleteDepartment(department_id)
        flash("Department Deleted Successfully!")
        return redirect(url_for('departmentList'))
    else:
        getdepartment = controller.getDepartment(department_id)
        return render_template('deletedepartment.html', 
                                department=getdepartment)

@app.route('/Deparment/<int:department_id>/new/', methods=['GET','POST'])
def newSeminarItem(department_id):
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['title'] and request.form['date_time']:
            dept = controller.getDepartment(department_id)

            # Form fields
            addTitle = request.form['title']
            addSpeaker = request.form['speaker']
            addDate = datetime.strptime(request.form['date_time'], '%d, %B %Y').date()
            addAbstract = request.form['abstract']
            addBuilding = request.form['building']
            addRoom = request.form['room']
            addDepartment = dept
            
            args = (addTitle, 
                    addSpeaker, 
                    addAbstract, 
                    addDate, 
                    addBuilding, 
                    addRoom,
                    addDepartment)

            # Add department to controller
            controller.addNewSeminar(*args)

            # Get department and seminar objects
            listOfSeminars = controller.getAllSeminarItems(department_id)
            flash("Seminar Added Successfully!")
        return redirect(url_for('departmentSeminars', 
                                department_id=dept.id))
    else:
        # From controller get a list of all items
        getdepartment = controller.getDepartment(department_id)
        listOfSeminars = controller.getAllSeminarItems(department_id)
        # render template
        return render_template('newseminar.html', 
                                department=getdepartment)

# Task 2: Create route for editSeminarItem function here

@app.route('/Deparment/<int:department_id>/<int:seminar_id>/edit/', methods=['GET','POST'])
def editSeminarItem(department_id, seminar_id):
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method =='POST':
              
        dept = controller.getDepartment(department_id)
        # Form fields
        addTitle = request.form['title']
        addSpeaker = request.form['speaker']
        addDate = datetime.strptime(request.form['date_time'], '%d, %B %Y').date()
        addAbstract = request.form['abstract']
        addBuilding = request.form['building']
        addRoom = request.form['room']
            
        args = (addTitle, 
                addSpeaker, 
                addAbstract, 
                addDate, 
                addBuilding, 
                addRoom,
                seminar_id)


        # edit seminar to controller
        controller.editSeminar(*args)
        flash("Seminar Edited Successfully!")
        getdepartment = controller.getDepartment(department_id)
        return redirect(url_for('departmentSeminars', 
                                department_id=getdepartment.id))
    else:
        getdepartment = controller.getDepartment(department_id)
        getseminar = controller.getSeminarItem(seminar_id)
        return render_template('editseminar.html', 
                                department=getdepartment,
                                seminar=getseminar)
    return "page to edit a seminar item. Task 2 complete!"

# Task 3: Create a route for deleteSeminarItem function here

@app.route('/Deparment/<int:department_id>/<int:seminar_id>/delete/', 
            methods=['GET','POST'])
def deleteSeminarItem(department_id, seminar_id):
    getSeminarUser = ""
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if getSeminarUser.user_id != login_session['user_id']:
        return """<script>function myFunction() { alert('You are not authorized
                  to delete this Seminar. Please create your own seminar in 
                  order to delete.');}</script><body onload='myFunction()'>
               """
    if request.method =='POST':
        # Delete department to controller
        controller.deleteSeminar(seminar_id)
        flash("Seminar Deleted Successfully!")
        getdepartment = controller.getDepartment(department_id)
        return redirect(url_for('departmentSeminars', 
                                department_id=getdepartment.id))
    else:
        getdepartment = controller.getDepartment(department_id)
        getseminar = controller.getSeminarItem(seminar_id)
        return render_template('deleteseminar.html', 
                                department=getdepartment,
                                seminar=getseminar)

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