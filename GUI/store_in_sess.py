#!/usr/bin/env python3

from cgi import FieldStorage, escape
from cgitb import enable
enable()
from shelve import open
from http.cookies import SimpleCookie
form_data = FieldStorage()

if len(form_data) != 0:
	token = form_data.getfirst("token")
	cookie = SimpleCookie()
	cookie['token'] = token
	session_store = open("/var/www/html/sessions/sess_" + token, writeback=True)
	session_store['authenticated'] = True
	session_store['token'] = token
	session_store.close()
	print(cookie)
	print("Content-Type: text/plain")
	print()
	print("good")
else:
	print("Content-Type: text/plain")
	print()
	print("problem")
