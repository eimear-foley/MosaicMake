#!/usr/bin/env python3

import cgi, os
from cgitb import enable
enable()
from cgi import FieldStorage
from hashlib import sha256
from time import time
from shelve import open
from PIL import Image
from http.cookies import SimpleCookie

sid = sha256(repr(time()).encode()).hexdigest()
			
cookie = SimpleCookie()
cookie['up_token'] = sid
print(cookie)
print("Location:http://143.239.81.202/cgi-bin/form.py")
print('Content-Type: text/html')
print()

form_data = FieldStorage()

# Get filename here.
fileitem = form_data['filename']

# Test if the file was uploaded
if fileitem.filename:
   # strip leading path from file name to avoid 
   # directory traversal attacks
   # fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
   # sid = sha256(repr(time()).encode()).hexdigest()
   mypath = '/var/www/html/tmp_fold/usr_' + sid
   if not os.path.isdir(mypath):
      os.makedirs(mypath)
      os.chmod(mypath, 0o777)
   # open(mypath + '/' + fn, 'wb').write(fileitem.file.read())
   img = Image.open(fileitem.file)
   img.save(mypath + '/profile.png')
   os.chmod(mypath + '/profile.png',0o777)

print("""
<!DOCTYPE html>
<head><title></title></head>
<body><p>%s</p></body>
</html>
""" % (mypath))
