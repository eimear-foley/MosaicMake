from PIL import Image, ImageFilter
from os import listdir
from os.path import isfile, join
from ColourCost import *
from mosaic1 import *
import timeit
from apitmp import *
import shutil
import tempfile

mypath = '/home/gabrielle/mosaic/'
#session_id = '123456789'
#rename variable 'temp' in line 14 to 'tmp' when using session_id
temp = tempfile.mkdtemp(prefix = 'temp') 
#os.rename(tmp,'/tmp/'+'%s' %(session_id)) 
#temp = '/tmp/' + session_id



def SplitImage(img, N):
    print("SPLIT IMAGE")
    try:
        im = Image.open(img)
    except FileNotFoundError:
        print("Error opening main image")
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
    
    rgb_value = get_rgb('resized.jpeg', N, w2, h2)
    tileWidth = w2 // N
    get_photos(tileWidth, temp)
    
    mosaic_images = [f for f in listdir(temp+"/") if isfile(
        join(temp+"/", f)) if not f.endswith('.DS_Store') if f.endswith('jpeg')]
    mosaic_images.sort()
    print(mosaic_images)
    rgbimg = []
    for img in mosaic_images:
        try:
            rgbimg += [get_average_color(0, 0, tileWidth, temp+"/"+ img)]
        except IOError:
            print("Error")
            continue
    # a list of tuples containging rgb values are stored in variable 'rgbimg'
    # returns a list of rgb values in tuples
    
    print(rgb_value, rgbimg)
    return rgb_value, rgbimg


def get_rgb(image, N, w, h):
    print("get rgb")
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
    print("DONE getrgb")
    return rgbimg


def get_average_color(w, h, n, image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner) 
    is (x, y) in the given image"""
    print("G_A_C")
    print(w, h)
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
    print("DONE GAC")
    return ((r // count), (g // count), (b // count))




def grid(nj, orgimage):
    print("GRID")
    mosaic_images = [f for f in listdir(temp+"/") if isfile(
        join(temp+"/", f)) if f != '.DS_Store' if f.endswith("jpeg")]
    mosaic_images.sort()
    print("LIST WITH IMAGES")
    tile = Image.open(temp+"/" + mosaic_images[0])
    w, h = tile.size  # width and height of tile
    print(w, h)
    orgimage = Image.open(mypath+orgimage)
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
            #im = Image.open(mypath + "mosaic_images/" + img)
            im = Image.open(temp+"/" + img)
            result.paste(im, (x, y))
            t += 1
            x += w
        y += h
    
    result.save(mypath + 'res.jpeg')
    im2 = Image.open('resized.jpeg') 
    im3 = im2.filter(ImageFilter.EDGE_ENHANCE_MORE)
    im3.save(mypath+'im3.jpeg')
    final = Image.blend(result, im3, 0.25)
    final.save(mypath + 'final.jpeg')
    #if os.path.isfile(temp+""):
    shutil.rmtree(temp+"/")
    #else:    
        #print("Error: %s/file not found" % temp)
    final.show()
    
si = SplitImage('kitty.jpeg', 50)
grid(Final(si), 'resized.jpeg')
