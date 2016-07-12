#!/usr/local/bin/python3


from cgi import FieldStorage, escape
from cgitb import enable
enable()
from http.cookies import SimpleCookie
from os import environ
from shelve import open
from mosaic_test import *
from api import *

cookie = SimpleCookie()
http_cookie_header = environ.get("HTTP_COOKIE")
if http_cookie_header:
    cookie.load(http_cookie_header)
    if "token" in cookie:
        token = cookie["token"].value
        session_store = open("sessions/sess_" + token, writeback = False)
        if session_store.get("authenticated"):
	    
            fileitem = graph.get_connections(profile['id'], 'picture')
            si = SplitImage(fileitem, 60)
            grid(Final(si), 'tmp_fold/usr_/' + token + '/resized.png', token)
            source = 'tmp_fold/usr_'+ token + '/final.png'
            
            
   	    else:
            #they aren't logged in
            source = 'Problem'
            

print("Content-Type: text/plain")
print()
print(source)
