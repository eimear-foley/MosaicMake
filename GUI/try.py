#!/usr/local/bin/python3

import pymysql as db
from cgi import FieldStorage, escape
from cgitb import enable
enable()
from http.cookies import SimpleCookie
from os import environ
from shelve import open

bigimg = ""
littleimgs = []
result = ""
message = ""
title=""

cookie = SimpleCookie()
http_cookie_header = environ.get("HTTP_COOKIE")
if http_cookie_header:
    cookie.load(http_cookie_header)
    if "sid" in cookie:
        sid = cookie["sid"].value
        session_store = open("sessions/sess_" + sid, writeback = False)
        if session_store.get("authenticated"):
	    form_data = FieldStorage()
	    if len(form_data) != 0:
	    	fileitem = form_data.getfirst("filename", "").strip()
            	if fileitem.filename:
  	 	    # strip leading path from file name to avoid 
   		    # directory traversal attacks
   		    fn = os.path.basename(fileitem.filename)
   		    filepath = "/tmp/temp_%s/" %(sid)
   		    open(filepath + fn, 'wb').write(fileitem.file.read())
                    title = "These images wil be used to make your mosaic!"
                    message = """Are you okay with these images? <a id="do_the_program">Yes</a> <a href="index.html">No</a>"""
   		    result += """<img id="bigimg" src="%s">"""%(filepath)
   		    result += """<div class="img_container">"""
   		    for img in listdir(filepath + "littleimgs/"):
   			imgpath = join(filepath + "littleimgs", img)
   			if isfile(imgpath):
   			    result += """<img src="%s">""" %(imgpath)
   			    result += "</div>"
			else:
                title = "Error"
   			    result = "<p>No file was uploaded</p>"
		else:
            title = "Upload your photo!"
		    result = """<form enctype="multipart/form-data" 
                        action="save_file.py" method="post">
   				        <p>File: <input type="file" name="filename" /></p>
   						<p><input type="submit" value="Upload" /></p>
   						</form>
						"""

print("Content-Type: text/html")
print()

print("""
    <!DOCTYPE html>
    <html>
        <head>
            <link href="default.css" rel="stylesheet" type="text/css" media="all" />
            <title>Try</title>
            <script src="try.js"></script>
        </head>
        <body>
            <a href="#" class="back-to-top"><br>Back to Top</a>
            <div id="header-wrapper">
                <div id="header" class="container">
                    <div id="logo">
                        <h1 style=" color: white;"> <img src="jigsaw.png" alt="jigsaw piece" height="25" width="25" >  MosaicMake</h1>
                    </div>
                    <div id="menu">
                        <ul>
                            <li class="active"><a href="#" accesskey="1" title="">Mosaic Builder</a></li>
                            <li><a href="#example" accesskey="2" title="">Examples</a></li>
                            <li><a href="#about" accesskey="3" title="">About Us</a></li>
                            <li><a href="#contact" accesskey="4" title="">Contact Us</a></li>
                            <li><a href="#social" accesskey="5" title="">Social Media</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="container">
                <div class="title">
                    <h2>%s</h2>
                </div>
                %s
                %s
            </div>
            <div id="copyright" class="container">
                <p>&copy; Untitled. All rights reserved. | released under the <a href="http://templated.co/license">Creative Commons Attribution</a> 
                license | Design by <a href="http://templated.co" rel="nofollow">TEMPLATED</a>.</p>
            </div>
        </body>
    </html>
""" % (title, message, result))
