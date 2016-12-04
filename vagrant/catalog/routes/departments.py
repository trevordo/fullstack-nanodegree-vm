import controller
import json

from datetime import datetime, date
from database import Department, Base, Seminar, User
from flask import Flask, render_template, request, redirect, url_for, \
                  flash, jsonify, make_response

from . import routes

# decorator wraps function into app.route function if any of these
# addresses get entered, the HelloWorld function gets executed
@routes.route('/')
@routes.route('/Department')
def departmentList():
    listOfDeparments = controller.getAllDepartments()
    return render_template('department.html', departments=listOfDeparments)


@routes.route('/Deparment/new/', methods=['GET','POST'])
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

@routes.route('/Deparment/<int:department_id>/edit/', methods=['GET','POST'])
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

@routes.route('/Deparment/<int:department_id>/delete/', methods=['GET','POST'])
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

@routes.route('/Deparment/<int:department_id>/new/', methods=['GET','POST'])
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