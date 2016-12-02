import controller

from flask import Flask, render_template, request, redirect,url_for, flash
# create instance of class with name of running application as arg
# anytime we run an application in python a special variable called
# name gets defined for the application an all of imports it uses
app = Flask(__name__)

# decorator wraps function into app.route function if any of these
# addresses get entered, the HelloWorld function gets executed
@app.route('/')
@app.route('/Deparment')
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

@app.route('/Deparment/new/')
def newDepartment():
    return "page to add Deparment"

@app.route('/Deparment/<int:department_id>/edit/', methods=['GET','POST'])
def editDeparment(department_id):
    if request.method =='POST':
        if request.form['name']:
            editName = request.form['name']
            editDesc = request.form['description']
        controller.editDepartment(department_id,editName,description)
        return redirect(url_for('departmentList'))
    else:
        getDeparmtnet = controller.getDepartment(department_id)
        return render_template('editDeparment.html', department=getDepartment)

@app.route('/Deparment/<int:department_id>/delete/', methods=['GET','POST'])
def deleteDepartment(department_id):
    return "page to delete Deparment"

@app.route('/Deparment/<int:department_id>/new/')
def newSeminarItem(department_id):
    return "page to create a new seminar item. Task 1 complete!"

# Task 2: Create route for editSeminarItem function here


@app.route('/Deparment/<int:department_id>/<int:seminar_id>/edit/')
def editSeminarItem(department_id, seminar_id):
    return "page to edit a seminar item. Task 2 complete!"

# Task 3: Create a route for deleteSeminarItem function here


@app.route('/Deparment/<int:department_id>/<int:seminar_id>/delete/')
def deleteSeminarItem(department_id, seminar_id):
    return "page to delete a seminar item. Task 3 complete!"


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