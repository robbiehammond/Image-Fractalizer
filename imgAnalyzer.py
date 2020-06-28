#projet - reconstruct one image from multiple other, or a single image
#if using a single image, change the image color and stuff so it fits
#use tkinter prolly
#save qtCreator for some c++ stuff
import matplotlib as plt
import numpy as np
from PIL import Image

im = Image.open('image0.jpg')

# resize image to be the nearest multiple of 9 in both dimensions
# we seem to be good!
def divideImg(inputIm):
    imAr = np.asarray(inputIm)
    width = imAr.shape[0]
    height = imAr.shape[1]

    while width % 9 != 0:
        width += 1
    while height % 9 != 0:
        height += 1
    finalIm = inputIm.resize((width, height))
    return finalIm


im = divideImg(im)
imAr = np.asarray(im)
print(imAr.shape)









def getAvgRGB(inputSquare):
    r = 0
    g = 0
    b = 0
    for pixel in inputSquare:
        r += pixel[0] # the r value of this pixel, etc
        g += pixel[1]
        b += pixel[2]
    #assuming I keep dividing the image into 9s
    r = int(r / 81)
    g = int(g / 81)
    b = int(b / 81)
    print((r,g,b))
    return (r, g, b)




#square list size = im.x/9 * im.y/9
squareList = []
for i in range(0, int(imAr.shape[0]/9)):
    squareList.append([])
    for j in range(0, int(imAr.shape[1]/9)):
        squareList[i].append([])


# for the xs, skipping 9 by each time, not going to the absoulte end but one before
# I think this will be a "down and then across" type strategy
#it somehow works
for i in range(0, imAr.shape[0], 9):
    for j in range(0, imAr.shape[1], 9):
        #now for the ind. square
        RGBvalsInSquare = []
        for k in range(0, 9):
            for l in range(0, 9):
                rgb = imAr[i+k][j+l]
                RGBvalsInSquare.append(rgb)  # should be 81 long
        squareList[int(i/9)][int(j/9)] = getAvgRGB(RGBvalsInSquare)

ar = np.asarray(squareList)
img = Image.fromarray(ar.astype(np.uint8))
width = imAr.shape[0]
height = imAr.shape[1]
img = img.resize((width, height))

im.show()
img.show()














'''tentative algo:
        -get the color of each and every pixel
        -find the average color of the 8(ish) surrounding pixels (ie a square)
            -reshape the image so that perfect squares of 9 pixels can be made
            -find color of each pixel, take avg of all 
        -edit other image to fit that color 
        -repeat for each
        -done 
'''