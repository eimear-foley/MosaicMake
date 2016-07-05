from PIL import Image, ImageFilter
from os import listdir
from os.path import isfile, join
from ColourCost import *
from mosaic1 import *
from get_rgb import *
from api import *

mypath = '/Users/claire/mosaic/'


def SplitImage(img, N):
    print("SPLIT IMAGE")
    try:
		im = Image.open(img)
	except FileNotFoundError:
		print('Error opening main image')
		exit()
    imgwidth, imgheight = im.size
    if imgwidth > imgheight:
        diff = imgwidth - imgheight
        d = imgheight - N * int(imgheight // N)
        resized = im.crop((0, 0, imgheight - d, imgheight - d))

    elif imgwidth < imgheight:
        d = imgwidth - N * int(imgwidth // N)
        resized = im.crop((0, 0, imgwidth - d, imgwidth - d))

    elif imgwidth == imgheight:
        d = imgheight - N * int(imgheight // N)
        resized = im.crop((0, 0, imgheight - d, imgheight - d))

    print('MAIN IMAGE RESIZED')
    resized.save(mypath + "resized.jpeg")
    im2 = Image.open(mypath + "resized.jpeg")
    w2, h2 = im2.size
    tileWidth = w2 // N
    rgb_value = get_rgb('resized.jpeg', N, w2, h2)
    # resize all the images used in the final mosaic
    get_photos(tileWidth)
    mosaic_images = [f for f in listdir(mypath + "mosaic_photos/") if isfile(
        join(mypath + "mosaic_photos/", f)) if not f.endswith('.DS_Store')]
    mosaic_images.sort()
    # a list of tuples containging rgb values are stored in variable 'rgbimg'
    # returns a list of rgb values in tuples
    rgbimg = []
    for img in mosaic_images:
        try:
            rgbimg += [get_average_color(0, 0, tileWidth, mypath + 'mosaic_photos/'+ img)]
        except IOError:
            print('Problem with %s' % (img))
			continue
    return rgb_value, rgbimg


def grid(nj, orgimage):
    mosaic_images = [f for f in listdir(mypath + "mosaic_photos/") if isfile(
        join(mypath + "mosaic_photos/", f)) if f != '.DS_Store']
    mosaic_images.sort()
    tile = Image.open(mypath + "mosaic_photos/" + mosaic_images[0])
    w, h = tile.size  # width and height of tile
    orgimage = Image.open(orgimage)
    total_w, total_h = orgimage.size
    # x = 0
    y = 0
    t = 0
    result = Image.new('RGB', (total_w, total_h))  # new image
    print(nj)
    len_nj = len(nj)
    while y + h <= total_h and t < len_nj:
        x = 0
        while x + w <= total_w:
            img = mosaic_images[nj[t][1]]
            im = Image.open(mypath + "mosaic_photos/" + img)
            result.paste(im, (x, y))
            t += 1
            x += w
        y += h
    
    result.save(mypath + 'res.jpeg')
    im2 = Image.open('resized.jpeg') 
    im3 = im2.filter(ImageFilter.EDGE_ENHANCE_MORE)
    im3.save(mypath+'im3.jpeg')
    final = Image.blend(result, im3, 0.25)
    final.save(mypath+'final.jpeg')
    final.show()
    
si = SplitImage('test.jpg', 100)
grid(Final(si), 'resized.jpeg')
