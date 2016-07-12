from PIL import Image, ImageFilter
import os
from os import listdir
from os.path import isfile, join
from ColourCost import *
from new_nj import *
import timeit
from api import *
import tempfile
import shutil


def SplitImage(img, N, token):
    try:
        im = Image.open(img)
    except FileNotFoundError:
        print('Error opening main image')
        exit()
        
    temp = os.makedirs('temp_fold/usr_'+token+'/images')
    temp = '/tmp/temps/'+token+'/images/'
    
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

    resized.save('/tmp_fold/usr_' + token + '/resized.png')

    im2 = Image.open('/tmp_fold/usr_' + token + '/resized.png')
    w2, h2 = im2.size
    
    rgb_original = get_rgb('resized.png', N, w2, h2)
    tileWidth = w2 // N
    get_photos(tileWidth, temp, token)#-- Photos are now collected when the access token is receicved
    
    
    mosaic_images = [f for f in listdir(temp+"/") if isfile(
        join(temp+"/", f)) if not f.endswith('.DS_Store') if f.endswith('png')]
    mosaic_images.sort()
    print(mosaic_images)
    rgb_images = []
    for img in mosaic_images:
        try:
            rgb_images += [get_average_color(0, 0, tileWidth, temp+"/"+ img)]
        except IOError:
            print("Error")
            continue
    
    
    print(rgb_original, rgb_images)
    return rgb_original, rgb_images


def get_rgb(image, N, w, h):
    div = w // N
    rgbimg = []
    htile = 0
    while htile < h:
        wtile = 0
        while wtile < w:
            r, g, b = get_average_color(wtile, htile, div, image)
            rgbimg += [(r, g, b)]
            wtile += div
        htile += div
    return rgbimg


def get_average_color(w, h, n, image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner) 
    is (x, y) in the given image"""
    image = Image.open(image).load()
    r, g, b = 0, 0, 0
    count = 0
    for s in range(w, w + n):
        for t in range(h, h + n):
            pixlr, pixlg, pixlb = image[s, t]
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1
    return ((r // count), (g // count), (b // count))


def grid(nj, orgimage, token):
    
    mosaic_images = [f for f in listdir('/tmp_fold/usr_' + token +'/images/') if isfile(
        join('/tmp_fold/usr_' + token +'/images/', f)) if f != '.DS_Store' if f.endswith("png")]
    tile = Image.open('/tmp_fold/usr_' + token +'/images/' + mosaic_images[0])
    w, h = tile.size  # width and height of tile
    print(w, h)
    orgimage = Image.open(orgimage)
    total_w, total_h = orgimage.size
    print(total_w, total_h)
    x = 0
    y = 0
    t = 0
    result = Image.new('RGB', (total_w, total_h))  # new image
    print(nj)
    len_nj = len(nj)
    while y + h <= total_h and t < len_nj:
        x = 0
        while x + w <= total_w:
            img = mosaic_images[nj[t][1]]
            im = Image.open(temp+"/" + img)
            result.paste(im, (x, y))
            t += 1
            x += w
        y += h
    result.save('/tmp_fold/usr_' + token + 'res.png')
    im2 = Image.open('resized.png') 
    im3 = im2.filter(ImageFilter.EDGE_ENHANCE_MORE)
    im3.save('/tmp_fold/usr_' + token +'im3.png')
    final = Image.blend(result, im3, 0.25)
    final.save('/tmp_fold/usr_' + token+'/final.png')
    final.show()

