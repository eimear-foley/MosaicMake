import requests
from io import BytesIO
from PIL import Image
import facebook
mypath = '/Users/claire/mosaic/mosaic_photos/'

def some_action(tileWidth, photo, p, i):
    #saves the photo in the folder 'photos' eg photos/0_0.jpeg
    
    response = requests.get(photo['source'])
    img = Image.open(BytesIO(response.content))
    print('size:',img.size)
    print(tileWidth)
    img = img.resize((tileWidth, tileWidth), Image.ANTIALIAS)
    img.save(mypath+"%i_%i.jpeg" %(p, i))
    return

def get_photos(tileWidth):
    # You'll need an access token here to do anything.  You can get a temporary one
    # here: https://developers.facebook.com/tools/explorer/
    access_token = 'EAACEdEose0cBAOu1rlrMH5Q9Hbgv1pvQZB92wLdYckTZANqZCj8Czi2yKToF29BVwYmpZBRn9EcZAPVY4I1M5rDptNk48hHIjdIZAbV4S34NMYQT9Fywbxt7CtDpwbNeJiEA4S62nEiqRt7lJMk1luzaZAEAF3uZA9tNE59ww2YhaQZDZD'
    # Look at my profile!
    user = 'me'

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)
    photos = graph.get_connections(profile['id'], 'photos')

    # Wrap this block in a while loop so we can keep paginating requests until
    # finished.
    page = -1
    while True:
        page += 1  
        try:
            # Perform some action on each photo in the collection we receive from
            # Facebook.
            img = 0
            for photo in photos['data']:
                some_action(tileWidth, photo, page, img)
                img += 1

            # Attempt to make a request to the next page of data, if it exists.
            photos = requests.get(photos['paging']['next']).json()    
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break
    print("Done!")
