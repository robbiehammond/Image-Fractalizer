# projet - reconstruct one image from multiple other, or a single image
# if using a single image, change the image color and stuff so it fits
# use tkinter prolly
# save qtCreator for some c++ stuff

'''
    So what is this project? It's an Image Reconstructor!
        - You can make images from other images
            -Works via lowering the quality of an image through "Pixel Approximation". The approximation scale is of the users choice
            -By cutting the image into squares of divSize x divSize pixels, each square takes on a single pixel color, effectively generalizing the rgb values within a given region of the picture
            -Another image is edited to fit the rgb values found in the generalized square region
        - You can apply weird functions (which I will think of) to each of the pixels in the image, changing the color, location, etc, effectively creating a new, weirder image
        - Create image from an array you input yourself? who knows
'''

# TODO - Scale image down before processing to reduce time it takes for extremely large images (maybe if the dimensions are both above 1000, ask the user if they'd like to scale the image down to save time)

import numpy as np
from PIL import Image


# make the image be divisible by some user-inputted number
def resizeImg(inputIm, num):
    imAr = np.asarray(inputIm)
    width = imAr.shape[1]
    height = imAr.shape[0]
    while width % num != 0:
        width += 1
    while height % num != 0:
        height += 1
    finalIm = inputIm.resize((width, height))
    return finalIm


# get the avg RGB value in some mini square
def getAvgRGB(inputSquare):
    r = 0
    g = 0
    b = 0
    for pixel in inputSquare:
        r += pixel[0]  # the r value of this pixel, etc
        g += pixel[1]
        b += pixel[2]
    # divide r g b by the number of pixels in the square - should be division number squared
    r = int(r / len(inputSquare))
    g = int(g / len(inputSquare))
    b = int(b / len(inputSquare))
    return (r, g, b)


# create the list of mini squares (which will be filled with the approximated pixels) with the appropriate number of indexes
def createSquareList(imAr, num):
    squareList = []
    for i in range(0, int(imAr.shape[0] / num)):
        squareList.append([])
        for j in range(0, int(imAr.shape[1] / num)):
            squareList[i].append([])
    return squareList


# traverses the image in standard format, skipping every 9. for each (x, y) stop the outer two 4 loops make we examine the smaller 9x9 square consisting of (x -> x + 8, y -> y + 8)
# and find the average rgb value. Then push that average into the approximated pixel square list
def getNewPixelAr(im, num):
    im = resizeImg(im, num)
    imAr = np.asarray(im)
    squareList = createSquareList(imAr, num)
    for i in range(0, imAr.shape[1], num):  # for x axis
        for j in range(0, imAr.shape[0], num):  # for y axis
            # now for the ind. square
            RGBvalsInSquare = []
            for k in range(0, num):  # for mini x axis
                for l in range(0, num):  # for mini y axis
                    rgb = imAr[j + k][i + l]
                    RGBvalsInSquare.append(rgb)  # should be 81 long
            squareList[int(j / num)][int(i / num)] = getAvgRGB(
                RGBvalsInSquare)  # img reconstruction is backwards (height, then width)
    return np.asarray(squareList)


def constructNewImg(img, divSize):
    # array of larger pixels
    pixelAr = getNewPixelAr(img, divSize)

    # start with a new, blank image the same size as the input image
    newImg = Image.new('RGB', img.size)
    # traverse larger pixels left to right, top to bottom
    for i in range(0, int(pixelAr.shape[1])):
        for j in range(0, pixelAr.shape[0]):
            # save the original image
            tempImg = img
            # resize it appropriately, based on the div size
            tempImg = tempImg.resize((divSize, divSize))
            # create a layer of the appropriate color based on the larger pixel ar, then put it on top of the image
            layer = Image.new('RGB', tempImg.size, (pixelAr[j][i][0], pixelAr[j][i][1], pixelAr[j][i][2]))
            tempImg = Image.blend(tempImg, layer, .5)
            # put this edited version of the original image at an apporpriate spot of the new image
            newImg.paste(tempImg, (divSize * i, divSize * j))
    return newImg


# combine all the functions above and run it in standard format
def fractalize(imgPath, divSize, savePath):
    divSize = int(divSize)  # is passed in as str from GUI, fix this l8r
    im = Image.open(imgPath)
    format = im.format
    im = im.convert('RGB') # make sure it is in RGB format before going on
    originalPixelAr = np.asarray(im)

    newImg = constructNewImg(im, divSize)
    newImg = newImg.resize((originalPixelAr.shape[1], originalPixelAr.shape[0]))
    newImg.save(savePath + '/FractalizedImg.' + str(format).lower(), str(format))
    return newImg

#fractalize('image0.jpg', 10, "C:/Users/Robbie/Desktop")
