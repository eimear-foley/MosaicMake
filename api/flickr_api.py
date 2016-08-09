import flickrapi
from PIL import Image
from io import BytesIO
import urllib.request
import os
os.environ['http_proxy']="http://4c.ucc.ie:80"
os.environ['https_proxy']="http://4c.ucc.ie:80"


def getPhotos(token, tags_list, tileWidth):
    path = '/var/www/html/tmp_fold/usr_'+token+'/images/'
    #path = '/var/www/html/demo/'
    if not os.path.isdir(path):
        os.makedirs(path)
        os.chmod(path, 0o777)
    api_key = u'c33f09d4aa3ad2ccc098139a2da21339'
    api_secret = u'5cabb635113d15a5'

    flickr = flickrapi.FlickrAPI(api_key, api_secret, store_token=False)
    limit = 0
    count = 0
    for tag in tags_list:
        limit += 25
        for photo in flickr.walk(tag_mode='all', tags=tag):
            count += 1
            if count <= limit:
                photo_id = photo.get('id')
                farm_id = photo.get('farm')
                server = photo.get('server')
                secret = photo.get('secret')
                url = 'http://farm' + farm_id + '.staticflickr.com/' + server + '/' + photo_id + '_' + secret + '.jpg'
                im = urllib.request.urlretrieve(url, path + 'test.png')
                im = Image.open(path + 'test.png')
                im = im.resize((tileWidth, tileWidth), Image.ANTIALIAS)
                im.save(path + '%s%s%s' % ('photo',count,'.png'), subsampling = 0, quality = 100)
                #im.save(path + '%sby%s' + '%s%s%s' % (num, num, 'photo',count,'.png'), subsampling = 0, quality = 100)
            else:
                break
    return
