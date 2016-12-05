import controller
import json

from datetime import datetime, date
from database import Department, Base, Seminar, User
from flask import Flask, render_template, request, redirect, url_for, \
                  flash, jsonify, make_response

from . import routes
from loginprovider import *

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
        return redirect(url_for('routes.departmentList'))
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
        return redirect(url_for('routes.departmentList'))
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
        return redirect(url_for('routes.departmentList'))
    else:
        getdepartment = controller.getDepartment(department_id)
        return render_template('deletedepartment.html', 
                                department=getdepartment)

