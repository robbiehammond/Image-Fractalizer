from PIL import Image, ImageEnhance
import numpy as np
import colorsys
import imgAnalyzer

img = Image.open('image0.jpg')
img.show()

#resize and then get the pixels for this image
img = imgAnalyzer.resizeImg(img, 5)
pixelAr = imgAnalyzer.getNewPixelAr(img, 5)


#make the array of copies of the appropriate length (1 pic for each new pixel)
#currently slow as shit, but working
copyAr = []
newImg = Image.new('RGB', (690,525))
for i in range(0, int(pixelAr.shape[1])):
   copyAr.append([])
   for j in range(0, pixelAr.shape[0]):
      copyAr[i].append([])
      tempImg = img
      tempImg = tempImg.resize((5,5))
      layer = Image.new('RGB', tempImg.size, (pixelAr[j][i][0], pixelAr[j][i][1], pixelAr[j][i][2]))
      tempImg = Image.blend(tempImg, layer, .5)
      copyAr[i][j] = tempImg
      newImg.paste(copyAr[i][j], (5 * j, 5 * i))


#mirrors, fix
newImg = newImg.transpose(Image.ROTATE_270)
newImg.show()
