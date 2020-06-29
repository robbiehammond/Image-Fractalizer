from PIL import Image, ImageEnhance
import numpy as np
import colorsys
import imgAnalyzer

#use imgenhance for blacks and whites
rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
   r, g, b, a = np.rollaxis(arr, axis=-1)
   h, s, v = rgb_to_hsv(r, g, b)
   h = hout
   r, g, b = hsv_to_rgb(h, s, v)
   arr = np.dstack((r, g, b, a))
   return arr

def colorize(image, hue):
   """
   Colorize PIL image `original` with the given
   `hue` (hue within 0-360); returns another PIL image.
   """
   img = image.convert('RGBA')
   arr = np.array(np.asarray(img).astype('float'))
   new_img = Image.fromarray(shift_hue(arr, hue/360.).astype('uint8'), 'RGBA')

   return new_img

img = Image.open('image0.jpg')

#resize and then get the pixels for this image
img = imgAnalyzer.resizeImg(img, 10)
pixelAr = imgAnalyzer.getNewPixelAr(img, 10)


#make the array of copies of the appropriate length (1 pic for each new pixel)
#currently slow as shit, but working
copyAr = []
for i in range(0, int(pixelAr.shape[0])):
   copyAr.append([])
   for j in range(0, pixelAr.shape[1]):
      copyAr[i].append([])
      tempImg = img
      filter = rgb_to_hsv(pixelAr[i][j][0], pixelAr[i][j][1], pixelAr[i][j][2])
      tempImg = colorize(tempImg, filter[0])
      copyAr[i][j] = tempImg
      print("here")

copyAr[5][5].show()



