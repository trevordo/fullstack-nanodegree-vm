import controller

from datetime import datetime, date
from database import Department, Base, Seminar
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# create instance of class with name of running application as arg
# anytime we run an application in python a special variable called
# name gets defined for the application an all of imports it uses
app = Flask(__name__)

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
    if request.method == 'POST':
        if request.form['title'] and request.form['date_time']:
            dept = controller.getDepartment(department_id)

            # Form fields
            addTitle = request.form['title']
            addSpeaker = request.form['speaker']
            addDate = datetime.strptime(request.form['date_time'], '%m/%d/%Y').date()
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
    if request.method =='POST':
              
        dept = controller.getDepartment(department_id)
        # Form fields
        addTitle = request.form['title']
        addSpeaker = request.form['speaker']
        addDate = datetime.strptime(request.form['date_time'], '%Y-%m-%d').date()
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

@app.route('/Deparment/<int:department_id>/<int:seminar_id>/delete/', methods=['GET','POST'])
def deleteSeminarItem(department_id, seminar_id):
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

# Making an API Endpoint (GET Request)
@app.route('/Department/<int:department_id>/seminar/JSON')
def departmentSeminarJSON(department_id):
    listOfSeminars = controller.getAllSeminarItems(department_id)   
    return jsonify(Seminars=[i.serialize for i in listOfSeminars])


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