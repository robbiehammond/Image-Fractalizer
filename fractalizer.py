import numpy as np
from PIL import Image

# TODO - Scale image down before processing to reduce time it takes for extremely large images (maybe if the dimensions are both above 1000, ask the user if they'd like to scale the image down to save time)
# TODO - Get better logo
# TODO - separate the functions in the construction of the image, and then have the dividingImage, fracalizing, and finishingUp changed only in fractalize(). Edit function parameters when necessary to get all info passed.

percentDone = 0
dividingImage = False
fractalizing = False
finishingUp = False


def getPercentDone():
    global percentDone
    return percentDone


def setPercentDone(percent):
    global percentDone
    percentDone = percent


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


# create the list of mini squares (which will be filled with the approximated pixels) with the appropriate number of
# indexes
def createSquareList(imAr, num):
    squareList = []
    for i in range(0, int(imAr.shape[0] / num)):
        squareList.append([])
        for j in range(0, int(imAr.shape[1] / num)):
            squareList[i].append([])
    return squareList


# traverses the image in standard format, skipping every n pixels. for each (x, y) pair, stop the outer two for loops
# We examine the smaller n x n square consisting of (x -> x + n, y -> y + n) (which is n^2 number of pixels) and find the average rgb value of that set of pixels
# Then push that average into the approximated pixel square list
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


def constructNewImg(img, divSize, pixelAr):
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
        setPercentDone(int((i / (pixelAr.shape[1] - 1)) * 100))
    return newImg


# combine all the functions above and run it in standard format
def fractalize(imgPath, divSize, savePath, name):
    divSize = int(divSize)
    im = Image.open(imgPath)
    imgFormat = im.format
    im = im.convert('RGB')
    originalPixelAr = np.asarray(im)

    global dividingImage
    dividingImage = True
    newPixelAr = getNewPixelAr(im, divSize)
    dividingImage = False

    global fractalizing
    fractalizing = True
    newImg = constructNewImg(im, divSize, newPixelAr)
    fractalizing = False

    global finishingUp
    finishingUp = True
    newImg = newImg.resize((originalPixelAr.shape[1], originalPixelAr.shape[0]))
    newImg.save(savePath + '/' + name + '.' + str(imgFormat).lower(), str(imgFormat))
    finishingUp = False
    return newImg
