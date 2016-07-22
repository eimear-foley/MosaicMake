#!/usr/bin/env python3

from cgitb import enable
enable()
from http.cookies import SimpleCookie
from os import environ
from shelve import open
from mosaic import *
import facebook
import requests
import os
from io import BytesIO
from PIL import Image
import tempfile
from nj import *

os.environ['http_proxy']="http://4c.ucc.ie:80"
os.environ['https_proxy']="http://4c.ucc.ie:80"
cookie = SimpleCookie()
http_cookie_header = environ.get("HTTP_COOKIE")
if http_cookie_header:
	cookie.load(http_cookie_header)
	if "token" in cookie:
		token = cookie["token"].value
		source = token
		session_store = open("sessions/sess_" + token, writeback = False)
		if session_store.get('authenticated'):
			try:
				temp = os.makedirs('tmp_fold/usr_' + token, mode = 0o777)
				temp = 'tmp_fold/usr_' + token
				source = temp
				os.chmod(temp, 0o777)
				temp = os.makedirs('tmp_fold/usr_' + token + '/images', mode = 0o777)
				temp2 = 'tmp_fold/usr_' + token + '/images'
				os.chmod(temp2, 0o777)
			except FileExistsError:
				source = "Error"
			user = "me"
			graph = facebook.GraphAPI(token)
			profile = graph.get_object(user)
			fileitem = graph.get_connections(profile['id'], 'picture', width=9999)
#			img_url = fileitem['url']
			response = requests.get(fileitem['url'])
			img = Image.open(BytesIO(response.content))
			img_path = 'tmp_fold/usr_' + token + '/profile.png'
			img.save(img_path)
			si = SplitImage(img_path, 10, token)
			source = grid(Final(si), 'tmp_fold/usr_' + token + '/resized.png', token)                   
#			source = 'tmp_fold/usr_'+ token + '/final.png'
			print('Content-Type: text/plain')
			print()
			print(source)
#		else:
#			# they aren't logged in
#			source = 'Problem'
