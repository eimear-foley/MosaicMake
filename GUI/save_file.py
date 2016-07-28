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

output = ''
status = False
form_data = FieldStorage()

if len(form_data) != 0:
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
		status = True

else:
	output = 'Please upload a file'
	status = False

if status:
	print("Location:http://143.239.81.202/cgi-bin/form.py")
print('Content-Type: text/html')
print()

print("""
<!DOCTYPE html>
<head><title>MosaicMake</title></head>
<body>
<div id='upload'>
	<form enctype="multipart/form-data" action="save_file.py" method="post">
		<p>Upload a photo:</p><br />
		<input id="file" type="file" name="filename" />
		<br />
		<p><input id="submit" type="submit" value="Upload" /></p><p>%s</p>
		</form>
	</div>
	 </body>
</html>""" % (output))
