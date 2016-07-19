import flickrapi
from PIL import Image
from io import BytesIO
import urllib.request
import os
os.environ['http_proxy']="http://4c.ucc.ie:80"
os.environ['https_proxy']="http://4c.ucc.ie:80"


def getPhotos(token, tag):
    path = '/tmp_fold/usr_'+token+'/images/'
    api_key = u'c33f09d4aa3ad2ccc098139a2da21339'
    api_secret = u'5cabb635113d15a5'

    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    limit = 50
    count = 0
    for photo in flickr.walk(tag_mode='all', tags=tag):
        if count <= limit:
            count += 1
            photo_id = photo.get('id')
            farm_id = photo.get('farm')
            server = photo.get('server')
            secret = photo.get('secret')
            url = 'http://farm' + farm_id + '.staticflickr.com/' + server + '/' + photo_id + '_' + secret + '.jpg'
            im = urllib.request.urlretrieve(url, path + 'test.png')
            im = Image.open(path + 'test.png')
            im.save(path + "test.png")
