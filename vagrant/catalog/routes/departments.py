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
    currentUser = login_session['user_id']
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method =='POST':
        if request.form['name'] and request.form['description']:
            addName = request.form['name']
            addDesc = request.form['description']
            addUser = currentUser.id
            # Add department to controller
            controller.addNewDepartment(addName,addDesc,addUser)
            flash("Department Added Successfully!")
        return redirect(url_for('routes.departmentList'))
    else:
        return render_template('newdepartment.html')

@routes.route('/Deparment/<int:department_id>/edit/', methods=['GET','POST'])
def editDepartment(department_id):
    getDepartmentUser = controller.getDepartmentUser(department_id)
    currentUser = login_session['user_id']
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if getDepartmentUser != currentUser.id:
        msg ="""You are not authorized to edit this Department. Please 
                create your own Department to edit!"""
        flash(msg)
        return redirect(url_for('routes.departmentList'))
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
    getDepartmentUser = controller.getDepartmentUser(department_id)
    currentUser = login_session['user_id']
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if getDepartmentUser != currentUser.id:
        msg = """You are not authorized to delete this Department. Please 
                 create your own Department to delete!"""
        flash(msg)
        return redirect(url_for('routes.departmentList'))
    if request.method =='POST':
        # Delete department to controller
        controller.deleteDepartment(department_id)
        flash("Department Deleted Successfully!")
        return redirect(url_for('routes.departmentList'))
    else:
        getdepartment = controller.getDepartment(department_id)
        return render_template('deletedepartment.html', 
                                department=getdepartment)

