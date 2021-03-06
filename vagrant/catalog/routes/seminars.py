import controller
import json

from datetime import datetime, date
from database import Department, Base, Seminar, User
from flask import Flask, render_template, request, redirect, url_for, \
                  flash, jsonify, make_response

from . import routes
from loginprovider import *

@routes.route('/Deparment/<int:department_id>/')
def departmentSeminars(department_id):
    # From controller get a list of all items
    getdepartment = controller.getDepartment(department_id)
    listOfSeminars = controller.getAllSeminarItems(department_id)
    # render template
    return render_template('seminars.html', 
                            department=getdepartment, 
                            items=listOfSeminars)

@routes.route('/Deparment/<int:department_id>/new/', methods=['GET','POST'])
def newSeminarItem(department_id):
    getDepartmentUser = controller.getDepartmentUser(department_id)
    currentUser = login_session['user_id']
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if getDepartmentUser != currentUser.id:
        flash("You are not authorized to add a Seminar. Please create your own Department to add a Seminar!")
        getdepartment = controller.getDepartment(department_id)
        return redirect(url_for('routes.departmentSeminars', 
                                department_id=getdepartment.id))
    if request.method == 'POST':
        if request.form['title'] and request.form['date_time']:
            dept = controller.getDepartment(department_id)

            # Form fields
            addTitle = request.form['title']
            addSpeaker = request.form['speaker']
            addDate = datetime.strptime(request.form['date_time'], '%d %B, %Y').date()
            addAbstract = request.form['abstract']
            addBuilding = request.form['building']
            addRoom = request.form['room']
            addUser = currentUser.id
            addDepartment = dept
            
            args = (addTitle, 
                    addSpeaker, 
                    addAbstract, 
                    addDate, 
                    addBuilding, 
                    addRoom,
                    addUser,
                    addDepartment)

            # Add department to controller
            controller.addNewSeminar(*args)

            # Get department and seminar objects
            listOfSeminars = controller.getAllSeminarItems(department_id)
            flash("Seminar Added Successfully!")
        return redirect(url_for('routes.departmentSeminars', 
                                department_id=dept.id))
    else:
        # From controller get a list of all items
        getdepartment = controller.getDepartment(department_id)
        listOfSeminars = controller.getAllSeminarItems(department_id)
        # render template
        return render_template('newseminar.html', 
                                department=getdepartment)

# Task 2: Create route for editSeminarItem function here

@routes.route('/Deparment/<int:department_id>/<int:seminar_id>/edit/', methods=['GET','POST'])
def editSeminarItem(department_id, seminar_id):
    getSeminarUser = controller.getSeminarItemUser(seminar_id)
    currentUser = login_session['user_id']
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if getSeminarUser != currentUser.id:
        flash("You are not authorized to Edit this Seminar. Please create your own seminar in order to Edit!")
        getdepartment = controller.getDepartment(department_id)
        return redirect(url_for('routes.departmentSeminars', 
                                department_id=getdepartment.id))
    if request.method =='POST':
              
        dept = controller.getDepartment(department_id)
        # Form fields
        addTitle = request.form['title']
        addSpeaker = request.form['speaker']
        addDate = datetime.strptime(request.form['date_time'], '%d %B, %Y').date()
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
        return redirect(url_for('routes.departmentSeminars', 
                                department_id=getdepartment.id))
    else:
        getdepartment = controller.getDepartment(department_id)
        getseminar = controller.getSeminarItem(seminar_id)
        return render_template('editseminar.html', 
                                department=getdepartment,
                                seminar=getseminar)
    return "page to edit a seminar item. Task 2 complete!"

# Task 3: Create a route for deleteSeminarItem function here

@routes.route('/Deparment/<int:department_id>/<int:seminar_id>/delete/', 
            methods=['GET','POST'])
def deleteSeminarItem(department_id, seminar_id):
    getSeminarUser = controller.getSeminarItemUser(seminar_id)
    currentUser = login_session['user_id']
    # Check to see if user is logged in to get to page
    if 'username' not in login_session:
        return redirect('/login')
    if getSeminarUser != currentUser.id:
        flash("You are not authorized to delete this Seminar. Please create your own seminar in order to delete!")
        getdepartment = controller.getDepartment(department_id)
        return redirect(url_for('routes.departmentSeminars', 
                                department_id=getdepartment.id))
    if request.method =='POST':
        # Delete department to controller
        controller.deleteSeminar(seminar_id)
        flash("Seminar Deleted Successfully!")
        getdepartment = controller.getDepartment(department_id)
        return redirect(url_for('routes.departmentSeminars', 
                                department_id=getdepartment.id))
    else:
        getdepartment = controller.getDepartment(department_id)
        getseminar = controller.getSeminarItem(seminar_id)
        return render_template('deleteseminar.html', 
                                department=getdepartment,
                                seminar=getseminar)