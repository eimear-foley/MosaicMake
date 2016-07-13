#!/usr/bin/env python3

from cgitb import enable
enable()

import cgi, os
from cgi import FieldStorage, escape
import pymysql as db

from page_layout import get_footer, get_admin_header
from protect_page import protect_admin

print('Content-Type: text/html')
print()

form_data = FieldStorage()
message = """<p>You do not have permissions to access this page.</p>
				<ul>
					<li><a href="register.py">Register</a></li>
					<li><a href="index.py">Login</a></li>
				</ul> """

try:
	# check if you have the permissions to access the protected page
	# must be an admin
	if protect_admin():
		# Get filename
		fileitem = form_data['filename']
		# get picture's name, price and tag
		name = escape(form_data.getfirst('picture_name', '').strip())
		price = escape(form_data.getfirst('price', '').strip())
		tag = escape(form_data.getfirst('tag', '').strip())

		# test if the file was uploaded
		if fileitem.filename:
			# strip leading path from file name to avoid 
			# directory traversal attacks
			fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
			open('pictures/' + fn, 'wb').write(fileitem.file.read())
			message = 'The file "' + fn + '" was uploaded successfully'

			# open the connection to the Database
			# put this between the try/except always
			connection = db.connect('cs1dev.ucc.ie', 'an11', 'aocoobei', '2019_an11')
			# create a cursor object for executing SQL statements
			cursor = connection.cursor(db.cursors.DictCursor)
			# insert the picture in the Database
			cursor.execute("""INSERT INTO pictures (picture, name, price, tag)
								VALUES (%s, %s, %s, %s)""" , ('<figure><img src="pictures/' + fn + '"></figure>', name, price, tag))
			# commit the connection to store it in the Database
			connection.commit()
			# close the cursor and the connection to the Database
			cursor.close()
			connection.close()
		# if no file has been uploaded
		else:
		   message = '<p>No file was uploaded %s</p>' % (fileitem.filename)
# if an error occurred
except IOError:
	message = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<title>White Cat</title>
			<link rel="icon" href="pictures/logo_trasparent.gif" type="image/x-icon">
			<link rel="stylesheet" href="main.css">
			<link href='https://fonts.googleapis.com/css?family=Poiret+One' rel='stylesheet' type='text/css'>
		</head>
		<body>
			%s
			%s
			%s
		</body>
	</html> """ % (get_admin_header(), message, get_footer()))
