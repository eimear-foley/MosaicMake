#!/usr/bin/env python3
from cgitb import enable
enable()
from cgi import FieldStorage, escape
from http.cookies import SimpleCookie
from os import environ
import os
from PIL import Image
import facebook
import requests
from io import BytesIO
import base64
os.environ['http_proxy']="http://4c.ucc.ie:80"
os.environ['https_proxy']="http://4c.ucc.ie:80"
source = ""
cookie = SimpleCookie()
http_cookie_header = environ.get("HTTP_COOKIE")
form_data = FieldStorage()
if http_cookie_header:
        cookie.load(http_cookie_header)
        token = cookie["token"].value
        mode = cookie["mode"].value
        source = token
        if mode == 'facebook':
                token = cookie["token"].value
                user = "me"
                graph = facebook.GraphAPI(token)
                profile = graph.get_object(user)
                fileitem = graph.get_connections(profile['id'], 'picture', width=9999)
                response = requests.get(fileitem['url'])
                img = Image.open(BytesIO(response.content))
                img.convert('RGB')
                img.save("/var/www/html/tmp_fold/usr_"+ token+ "/profile.png")
                source = token
        elif mode == "upload" and len(form_data) != 0:
                mypath = "/var/www/html/tmp_fold/usr_" + token
                if not os.path.isdir(mypath):
                        os.makedirs(mypath)
                        os.chmod(mypath, 0o777)
                path = mypath + "/profile.png"
                image = escape(form_data.getfirst("image", "").strip())
                image = image.split(',')
                image = image[1]
                image = str.encode(image)
                with open( path , "wb") as fh:
                        fh.write(base64.decodestring(image))
                im = Image.open(path)
                im.convert("RGB").save(path)
 


print("Content-Type: text/html")
print()
print("""
<!DOCTYPE html>
<html lang="en" class="no-js">
        <head>
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta name="description" content="Learn how to resize images using JavaScript and the HTML5 Canvas element using controls, commonly seen in photo editing applications." />
                <meta name="keywords" content="canvas, javascript, HTML5, resizing, images" />
                <meta name="author" content="Codrops" />
                <link rel="shortcut icon" href="../favicon.ico">
                <link rel="stylesheet" type="text/css" href="/normalize.css" />
                <link rel="stylesheet" type="text/css" href="/demo.css" />
                <link rel="stylesheet" type="text/css" href="/component.css" />
                <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
                <!--[if IE]>
                <title>MosaicMake</title>
                <link href="../jigsaw.png" rel="icon" />
                <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
                <![endif]-->
                <style>
                        body{
                                font-family: 'Source Sans Pro', sans-serif;
                        }
                </style>
        </head>
        <body>
                <div class="container">
                        <!-- Top Navigation -->
                        <div style="margin-right: auto; margin-left: auto;"><p style="text-align: center; font-size: 25px;">Please crop your photo to make your mosaic!</p></div>
                        <div class="content">
                                <div class="component">
                                        <div class="overlay">
                                                <div class="overlay-inner">
                                                </div>
                                        </div>
                                        <img class="resize-image" src="../tmp_fold/usr_%s/profile.png" alt="image for resizing">
                                        <button style="height: 50px; width: 150px; font-size: 20px;" class="btn-crop js-crop">Crop</button>
                                        <form class="next" style="" method="post" action="form.py">
                                                <input type="hidden" name="url" value="" id="url">
                                                <input type="submit" style="" id="url-submit" disabled>
                                        </form>

                                </div>
                        </div>
                </div>

                <script src="../jquery.js"></script>
                <script src="../component.js"></script>


        </body>
</html>
"""%(source))
