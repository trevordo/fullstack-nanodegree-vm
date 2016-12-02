from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# common gateway interface library
import cgi

#from controller import getAllRestaurants, addNewRestaurant, getRestaurantName
import controller

class WebServerHandler(BaseHTTPRequestHandler):
    # handles all request webserver recieves looking at the ending
    def do_GET(self):
        # contains url sent to server as string ending with /hello
        if self.path.endswith("/restaurants"):
            # server sends reponse 200 indicating successful GET request
            self.send_response(200)
            # replying as text in html 
            self.send_header('Content-type', 'text/html')
            # send blank line stops headers
            self.end_headers()
            # From controller get a list of all restaurants
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
            self.wfile.write(output)
            # helps exit if statement
            return
        # another url    
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += """<html><body><a href = '/restaurants'>
                        Back to Restaurants</a>"""
            output += """<form method='POST' enctype='multipart/form-data'>
                         <h2>Enter a new Restaurant:
                         </h2><input name='name' type='text' 
                         placeholder= " New Restaurant name">
                         <input type='submit' value='Submit'></form>
                      """
            output +="</body></html>"
            self.wfile.write(output)
            return
        
        if self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[2]
            name = controller.getRestaurantName(restaurantIDPath)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += """<html><body><a href = '/restaurants'>
                        Back to Restaurants</a>"""
            output += """<form method='POST' enctype='multipart/form-data'
                         action='/restaurants/%s/edit'>
                         <h2>Edit Restaurant name:
                         </h2><input name='name' type='text' 
                         placeholder= "%s">
                         <input type='submit' value='Rename'></form>
                      """ % (restaurantIDPath,name)
            output +="</body></html>"
            self.wfile.write(output)
            return

        if self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[2]
            name = controller.getRestaurantName(restaurantIDPath)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += """<html><body><a href = '/restaurants'>
                        Back to Restaurants</a>"""
            output += """<form method='POST' enctype='multipart/form-data'
                         action='/restaurants/%s/delete'>
                         <h2>Delete %s, Are you Sure?</h2>
                         <input type='submit' value='Delete'></form>
                      """ % (restaurantIDPath,name)
            output +="</body></html>"
            self.wfile.write(output)
            return
        
        else:
            # notifying of a 404 error
            self.send_error(404, "File Not Found %s" % self.path)
        
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                # parses html form header 
                ctype, pdict = cgi.parse_header(self.headers.\
                               getheader('content-type'))
                # checks to see if it's form data being submitted
                if ctype == 'multipart/form-data':
                    # collects all field
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    # get field 
                messagecontent = fields.get('name')
                controller.addNewRestaurant(messagecontent[0])

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):
                # parses html form header 
                ctype, pdict = cgi.parse_header(self.headers.\
                               getheader('content-type'))
                # checks to see if it's form data being submitted
                if ctype == 'multipart/form-data':
                    # collects all field
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    # get field 
                messagecontent = fields.get('name')
                editName = messagecontent[0]
                restaurantIDPath = self.path.split("/")[2]
                controller.editRestaurant(restaurantIDPath,editName)
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/delete"):
                # parses html form header 
                ctype, pdict = cgi.parse_header(self.headers.\
                               getheader('content-type'))
                restaurantIDPath = self.path.split("/")[2]
                controller.deleteRestaurant(restaurantIDPath)
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

                return
        except:
            pass

# entry part of the code
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), WebServerHandler)
        print "Web server running on port %s" % port
        # built into HTTPServer to listen constantly
        server.serve_forever()


    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        # stopping server
        server.socket.close()


# placed at the end to run main why interpreter runs script
if __name__ == '__main__':
    main()