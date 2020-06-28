#projet - reconstruct one image from multiple other, or a single image
#if using a single image, change the image color and stuff so it fits
#use tkinter prolly
#save qtCreator for some c++ stuff
import matplotlib as plt
import numpy as np
from PIL import Image

# TODO make it so that the pixel divisions can be inputted by user (ie not just 9, but whatever as long as it's less than the image size)


def lowerImgQuality(imgPath):
    im = Image.open(imgPath)
    originalPixelAr = np.asarray(im)
    im.show()

    #resize the img to be a good multiple
    im = resizeImg(im)

    #make the new image using the old image pixel array for size, and the new array for content
    newIm = constructNewIm(originalPixelAr, getNewPixelAr(im))

    newIm.show()


#make the image be divisible by some user-inputted number
# TODO all size to be resizable from 9 to whatever
def resizeImg(inputIm):
    imAr = np.asarray(inputIm)
    width = imAr.shape[1]
    height = imAr.shape[0]
    while width % 9 != 0:
        width += 1
    while height % 9 != 0:
        height += 1
    finalIm = inputIm.resize((width, height))
    return finalIm

# get the avg RGB value in some mini square
def getAvgRGB(inputSquare):
    r = 0
    g = 0
    b = 0
    for pixel in inputSquare:
        r += pixel[0] # the r value of this pixel, etc
        g += pixel[1]
        b += pixel[2]
    # divide r g b by the number of pixels in the square - should be division number squared
    r = int(r / 81)
    g = int(g / 81)
    b = int(b / 81)
    return (r, g, b)

# create the list of mini squares (which will be filled with the approximated pixels) with the appropriate number of indexes
def createSquareList(imAr):
    squareList = []
    for i in range(0, int(imAr.shape[0] / 9)):
        squareList.append([])
        for j in range(0, int(imAr.shape[1] / 9)):
            squareList[i].append([])
    return squareList


# traverses the image in standard format, skipping every 9. for each (x, y) stop the outer two 4 loops make we examine the smaller 9x9 square consisting of (x -> x + 8, y -> y + 8)
# and find the average rgb value. Then push that average into the approximated pixel square list
def getNewPixelAr(im):
    imAr = np.asarray(im)
    squareList = createSquareList(imAr)
    for i in range(0, imAr.shape[1], 9): # for x axis
        for j in range(0, imAr.shape[0], 9): # for y axis
            # now for the ind. square
            RGBvalsInSquare = []
            for k in range(0, 9): # for mini x axis
                for l in range(0, 9): # for mini y axis
                    rgb = imAr[j + k][i + l]
                    RGBvalsInSquare.append(rgb)  # should be 81 long
            squareList[int(j / 9)][int(i / 9)] = getAvgRGB(RGBvalsInSquare) # img reconstruction is backwards (height, then width)
    return np.asarray(squareList)


# construct the new image from the new array, using the width and height of the original image to resize
def constructNewIm(oldImAr, newImAr):
    newImg = Image.fromarray(newImAr.astype(np.uint8))
    width = oldImAr.shape[1]
    height = oldImAr.shape[0]
    newImg = newImg.resize((width, height))
    return newImg

lowerImgQuality('test.jpg')














'''tentative algo:
        -get the color of each and every pixel
        -find the average color of the 8(ish) surrounding pixels (ie a square)
            -reshape the image so that perfect squares of 9 pixels can be made - worked
            -find color of each pixel, take avg of all - worked
        -edit other image to fit that color 
        -repeat for each
        -done 
'''