from PIL import Image
import image_slicer
from os import listdir
from os.path import isfile,join

def SplitImage(img,num_tile):
   #creates tiles from image given
   #returns a list of tuples of rgb values 
   #directory in where the image we want to use is
   #to be changed accordingly
   mypath= '/home/gabrielle/tiles'
   #image is split into equally sized tiles
   tiles = image_slicer.slice(img, num_tile, save = False)
   #saves files in directory
   image_slicer.save_tiles(tiles, directory='/home/gabrielle/tiles', prefix='slices')
   #stores a list of sorted tiles in variable 'onlyfiles' with file extension '.png'
   tile_img = [f for f in listdir(mypath) if isfile(join(mypath, f))  if f.endswith(".png")]
   #sorting 'onlyfiles' to keep the order for the tiles
   tile_img.sort()
   # a list of tuples containging rgb values are stored in variable 'rgbtiles'
   rgbtiles = most_frequent_color(tile_img)
   #stores the resized images in a variable ''
   rgbimg = ResizeImg(tile_img[0])
   # a list of tuples containging rgb values are stored in variable 'rgbimg'
   #returns a list of rgb values in tuples
   return rgbtiles,rgbimg


   
def most_frequent_color(lst):
   # Finds most frequntly occuring color
   # in each image in the list
   
   rgb = []
   for image in lst:
       img = Image.open(image)
       w, h = img.size
       pixels = img.convert('RGB').getcolors(w*h)
       most_frequent_pixel = pixels[0]
       for count, color in pixels:
           if count > most_frequent_pixel[0]:
               most_frequent_pixel = (count, color)
       rgb += [most_frequent_pixel[1]]
   return rgb

def ResizeImg(image):
   # Resizes all images in lst to the size of
   # the split tiles of the original image
   #returns list of tuples containing rgb values
   
   #directory of the pictures for the mosaic
   #to be changed accordingly
   mypath = '/home/gabrielle/tiles/'
   #list of
   lst = [f for f in listdir(mypath) if isfile(join(mypath, f))  if not f.startswith('index4') if f.endswith(".jpeg")]
   lst.sort()
   lst2 = []
   i = Image.open(image)
   w,h = i.size

   for im in lst:
       lst2 += most_frequent_color([im])
       img = Image.open(im)
       #resizes images
       img = img.resize((w,h), Image.ANTIALIAS)
       #saves resized images in mypath
       img.save(mypath+im)
   return lst2

def grid(orgimage,tile,img):
   #nj = [(0,3), (1,0), (2,2),(3,1)]
   mypath = '/home/gabrielle/tiles/'
   #lst = ['slices_01_01.png', 'slices_01_02.png', 'slices_02_01.png', 'slices_02_02.png']
   lst = [f for f in listdir(mypath) if isfile(join(mypath, f))  if not f.startswith(img) if f.endswith(".jpeg")]
   lst.sort()

   tile = Image.open(tile)
   w,h = tile.size # width and height of tile
   orgimage = Image.open(orgimage)
   total_w, total_h = orgimage.size
   x=0
   y=0
   result = Image.new('RGB', (total_w,total_h)) # new image
   for pos in nj:
      img = lst[pos[1]]
      img = Image.open(img)
      if x < total_w and y < total_h:
         result.paste(img,(x,y))
         x += w
      elif y < total_h:
         x = 0
         y += h
         result.paste(img,(x,y))
         x += w
   result.save(mypath+'final.jpeg')
   result.show()


