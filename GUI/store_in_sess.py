#!/usr/lib/env python3

from cgi import FieldStorage, escape
from cgitb import enable
enable()
from shelve import open
from http.cookies import SimpleCookie

form_data = FieldStorage()
if len(form_data) != 0:
	token = escape(form_data.get_first("token", "").strip())
	cookie = SimpleCookie()
	cookie['token'] = token
	session_store = open("sessions/sess_" + token, writeback=True)
	session_store['authenticated'] = True
	session_store['token'] = token
	session_store.close()
	print("good")
else:
	print("problem")
