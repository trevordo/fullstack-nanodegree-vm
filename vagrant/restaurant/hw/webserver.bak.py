from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# common gateway interface library
import cgi


class WebServerHandler(BaseHTTPRequestHandler):
    # handles all request webserver recieves looking at the ending
    def do_GET(self):
        # contains url sent to server as string ending with /hello
        if self.path.endswith("/hello"):
            # server sends reponse 200 indicating successful GET request
            self.send_response(200)
            # replying as text in html 
            self.send_header('Content-type', 'text/html')
            # send blank line stops headers
            self.end_headers()
            # content sent to client
            output = ""
            output += "<html><body>Hello!"
            output += """<form method='POST' enctype='multipart/form-data'
                         action='/hello'><h2>What would you like me to say?
                         </h2><input name='message' type='text'><input 
                         type='submit' value='Submit'></form>
                      """
            output +="</body></html>"
            # send message to client
            self.wfile.write(output)
            print output
            # helps exit if statement
            return
        # another url    
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += """<html><body> &#161 Hola ! <a href = '/hello'>
                        Back to Hello</a>"""
            output += """<form method='POST' enctype='multipart/form-data'
                         action='/hello'><h2>What would you like me to say?
                         </h2><input name='message' type='text'><input 
                         type='submit' value='Submit'></form>
                      """
            output +="</body></html>"
            self.wfile.write(output)
            print output
            return
        
        else:
            # notifying of a 404 error
            self.send_error(404, "File Not Found %s" % self.path)
        
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            # parses html form header 
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # checks to see if it's form data being submitted
            if ctype == 'multipart/form-data':
                # collects all field
                fields = cgi.parse_multipart(self.rfile, pdict)
                # get field 
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how aobut this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            # form
            output += """<form method='POST' enctype='multipart/form-data'
                         action='/hello'><h2>What would you like me to say?
                         </h2><input name='message' type='text'><input 
                         type='submit' value='Submit'></form>
                      """
            output +="</body></html>"
            self.wfile.write(output)
            print output

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