import controller

from flask import Flask, render_template, request, redirect,url_for, flash
# create instance of class with name of running application as arg
# anytime we run an application in python a special variable called
# name gets defined for the application an all of imports it uses
app = Flask(__name__)

# decorator wraps function into app.route function if any of these
# addresses get entered, the HelloWorld function gets executed
@app.route('/')
@app.route('/restaurants')
def restaurant_list():
    listOfRestaurants = controller.getAllRestaurants()
    return render_template('restaurants.html', restaurants=listOfRestaurants)


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # From controller get a list of all items
    getrestaurant = controller.getRestaurant(restaurant_id)
    listOfMenuItems = controller.getMenuItem(restaurant_id)
    # render template
    return render_template('menu.html', 
                            restaurant=getrestaurant, 
                            items=listOfMenuItems)

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    if request.method =='POST':
        if request.form['name']:
            editName = request.form['name']
        controller.editRestaurant(restaurant_id,editName)
        return redirect(url_for('restaurant_list'))
    else:
        getrestaurant = controller.getRestaurant(restaurant_id)
        return render_template('editrestaurant.html', restaurant=getrestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    return "page to delete restaurant"

@app.route('/restaurant/new/')
def newRestaurant():
    return "page to add restaurant"

@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


# the application run by the python interpreter gets a name variable
# set to __main__ where all other imported python files gets __name__
# variable set to actual name of python file
# if statement here makes sure the server runs only if the script is executed
# directly from the python interpreter and not used as an imported module
# if imported dont do if statement but access to rest of the code available
if __name__ == '__main__':
    # helpful debugger so webserver doesnt need to be restarted
    app.secret_key = "Super_Secret_Key"
    app.debug = True
    # run function to run local server 
    app.run(host='0.0.0.0', port=5000)