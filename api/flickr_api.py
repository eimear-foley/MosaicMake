import flickrapi
from PIL import Image
from io import BytesIO
import urllib.request

mypath = '/Users/alessianardotto/Numberjack/Numberjack/insight-project/'


api_key = u'c33f09d4aa3ad2ccc098139a2da21339'
api_secret = u'5cabb635113d15a5'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

count = 0
for photo in flickr.walk(tag_mode='all', tags='smile'):
	count += 1
	photo_id = photo.get('id')
	farm_id = photo.get('farm')
	server = photo.get('server')
	secret = photo.get('secret')
	url = 'http://farm' + farm_id + '.staticflickr.com/' + server + '/' + photo_id + '_' + secret + '.jpg'
	print(url)
	if count == 1:
		im = urllib.request.urlretrieve(url, mypath + 'test.png')
		#im.save(mypath + "test.png")
		im = Image.open(mypath + 'test.png')
		im.show()
		break
