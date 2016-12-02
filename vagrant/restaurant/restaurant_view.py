import controller

def restaurant_list():
    listOfRestaurants = controller.getAllRestaurants()
    # content sent to client
    output = ""
    output += "<html><body>"
    output += """<div><a href='/restaurants/new'>
                 Add a new Restaurant</a></div>"""
    for restaurant in listOfRestaurants:
        output += "</br></div>"
        output += restaurant.name
        output += "</br><a href='/restaurants/%s/edit'>Edit</a>" \
                   % restaurant.id
        output += "</br><a href='/restaurants/%s/delete'>Delete</a>" \
                   % restaurant.id
        output += "</br></div>"
        output +="</body></html>"
        # send message to client
    return output

def restaurantMenu(restaurant_id):
    # From controller get a list of all restaurants
    listOfMenuItems = controller.getMenuItem(restaurant_id)
    # content sent to client
    output = ""
    output += "<html><body>"
    output += """<div><a href='/restaurants/new'>
                Add a new Restaurant</a></div>"""
    for i in listOfMenuItems:
        output += "</br></div>"
        output += i.name
        output += "</br>"
        output += i.price
        output += "</br>"
        output += i.description
        output += "</br><a href='/restaurants/%s/edit'>Edit</a>" \
                   % i.id
        output += "</br><a href='/restaurants/%s/delete'>Delete</a>" \
                   % i.id
        output += "</br></div>"
        output +="</body></html>"

    return output