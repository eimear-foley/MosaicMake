#!/usr/bin/env python3

from cgitb import enable
enable()
from http.cookies import SimpleCookie
from os import environ
from shelve import open
from mosaic import *
from mosaic_demo import *
import facebook
import requests
import os
from io import BytesIO
from PIL import Image
import tempfile
from nj import *
from cgi import FieldStorage, escape
os.environ['http_proxy']="http://4c.ucc.ie:80"
os.environ['https_proxy']="http://4c.ucc.ie:80"


form_data = FieldStorage()
photos = escape(form_data.getfirst("photos","").strip())
tags = form_data.getlist("tags")
premade = escape(form_data.getfirst("premade", "").strip())
opacity = escape(form_data.getfirst("opacity","").strip())

cookie = SimpleCookie()
http_cookie_header = environ.get("HTTP_COOKIE")
if http_cookie_header:
        cookie.load(http_cookie_header)
        if "token" in cookie:
                token = cookie["token"].value
                source = token
                usr_fold = '/var/www/html/tmp_fold/usr_' + token
                if premade == "false":
                        try:
                                temp = os.makedirs(usr_fold, mode = 0o777)
                                os.chmod(usr_fold, 0o777)
                                temp = os.makedirs(usr_fold + '/images', mode = 0o777)
                                os.chmod(usr_fold + '/images', 0o777)
                        except FileExistsError:
                                source = "Error"
                        si = SplitImage(usr_fold + '/profile.png', int(photos), token, tags)
                        source = si
                        if si == 'Tags no good':
                                source = 'There was a problem with the tags chosen. Please try again with different tags.'
                        else:
                                source = grid(Final(si), usr_fold + '/resized.png', token, opacity)
                                source = '../tmp_fold/usr_'+ token + '/final.png'
                        print('Content-Type: text/plain')
                        print()
                        print(source)
                elif premade == "true":
                        path = '%sby%s' %(photos, photos)
                        si = SplitImage2(usr_fold + '/profile.png', int(photos), token)
                        source = si
                        source = grid2(Final(si), usr_fold + '/resized.png', token, opacity, int(photos))
                        source = '../tmp_fold/usr_'+ token + '/final.png'
                        print('Content-Type: text/plain')
                        print()
                        print(source)
                else:
                        source = premade
                        print('Content-Type: text/plain')
                        print()
                        print(source)
