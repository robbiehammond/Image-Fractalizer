import numpy as np
from PIL import Image
import math


percentDone = 0
dividingImage = False
fractalizing = False
finishingUp = False
mustStop = False
maxThreshold = 400000  # good value found through trial and error 


def getPercentDone():
    global percentDone
    return percentDone


def setPercentDone(percent):
    global percentDone
    percentDone = percent


def stopASAP():
    global mustStop
    mustStop = True


def isAboveThreshold(imgPath, num):
    inputIm = Image.open(imgPath)
    imAr = np.asarray(inputIm)
    width = imAr.shape[1]
    height = imAr.shape[0]
    return (width * height) / int(num) > maxThreshold


# shrink image to get it below threshold
def forceBelowThreshold(inputIm, num):
    num = int(num)
    imAr = np.asarray(inputIm)
    width = imAr.shape[1]
    height = imAr.shape[0]
    while (width * height) / num > maxThreshold:
        # want to keep proportions the same, so img must be shrunk by a factor of sqrt(2) (from pythagoras theorem)
        # 1/30 is somewhat arbitrary - gets below threshold quick but doesn't "overshoot" getting below it much
        # a smaller value could technically work more accurately, but the difference seems to be negligible past 1/30
        width -= (1 / 30) * (math.sqrt(1 / 2) * width)
        height -= (1 / 30) * (math.sqrt(1 / 2) * height)

    width = int(width)
    height = int(height)

    notLargeIm = inputIm.resize((width, height))
    notLargeIm.format = inputIm.format  # format is lost when resizing, so must be reassigned
    return notLargeIm


# make the image be divisible by the div size by making it slightly larger
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
        r += pixel[0]
        g += pixel[1]
        b += pixel[2]
    # divide r g b by the number of pixels in the square - should be division number squared
    r = int(r / len(inputSquare))
    g = int(g / len(inputSquare))
    b = int(b / len(inputSquare))
    return (r, g, b)


'''create the list of mini squares (which will be filled with the approximated pixels) with the appropriate number of
   indexes'''
def createSquareList(imAr, num):
    squareList = []
    for i in range(0, int(imAr.shape[0] / num)):
        squareList.append([])
        for j in range(0, int(imAr.shape[1] / num)):
            squareList[i].append([])
    return squareList


''' traverses the image in standard format, skipping every n pixels. for each (x, y) pair, stop the outer two for loops
    We examine the smaller n x n square consisting of (x -> x + n, y -> y + n) (which is n^2 number of pixels) and 
    find the average rgb value of that set of pixels. Then push that average into the approximated pixel square list '''
def getNewPixelAr(im, num):
    global mustStop
    imAr = np.asarray(im)
    squareList = createSquareList(imAr, num)

    for i in range(0, imAr.shape[1], num):  # for x axis
        if mustStop:  # check if we should stop every so often
            return None
        for j in range(0, imAr.shape[0], num):  # for y axis

            # now for the ind. square
            RGBvalsInSquare = []

            for k in range(0, num):  # for mini x axis
                for l in range(0, num):  # for mini y axis
                    rgb = imAr[j + k][i + l]
                    RGBvalsInSquare.append(rgb)  # should be 81 long

            ''' (j, i) instead of (i, j) because PIL was designed with dimensions being (height, width) rather
                than (width, height) '''
            squareList[int(j / num)][int(i / num)] = getAvgRGB(RGBvalsInSquare)

    return np.asarray(squareList)


def constructNewImg(img, divSize, pixelAr):
    global mustStop

    # start with a new, blank image the same size as the input image
    newImg = Image.new('RGB', img.size)

    # traverse larger pixels left to right, top to bottom
    for i in range(0, int(pixelAr.shape[1])):
        if mustStop:
            return None
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

        setPercentDone(int((i / (pixelAr.shape[1] - 1)) * 100))

    return newImg


# where the magic happens
def fractalize(im, divSize, savePath, name):
    global mustStop
    mustStop = False
    divSize = int(divSize)  # comes in as str
    imgFormat = im.format
    im = im.convert('RGB')
    originalPixelAr = np.asarray(im)

    im = resizeImg(im, divSize)

    # many checks to see if the program was told to halt - if it was, break out of the function
    if mustStop:
        return

    global dividingImage
    dividingImage = True
    newPixelAr = getNewPixelAr(im, divSize)
    dividingImage = False

    if mustStop:
        return

    global fractalizing
    fractalizing = True
    newImg = constructNewImg(im, divSize, newPixelAr)
    fractalizing = False

    if mustStop:
        return

    global finishingUp
    finishingUp = True
    newImg = newImg.resize((originalPixelAr.shape[1], originalPixelAr.shape[0]))
    newImg.save(savePath + '/' + name + '.' + str(imgFormat).lower(), str(imgFormat))
    finishingUp = False

    if mustStop:
        return

    return newImg
