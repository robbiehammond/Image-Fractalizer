#projet - reconstruct one image from multiple other, or a single image
#if using a single image, change the image color and stuff so it fits
#use tkinter prolly
#save qtCreator for some c++ stuff

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

#make the image be divisible by some user-inputted number
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
        r += pixel[0] # the r value of this pixel, etc
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
    for i in range(0, imAr.shape[1], num): # for x axis
        for j in range(0, imAr.shape[0], num): # for y axis
            # now for the ind. square
            RGBvalsInSquare = []
            for k in range(0, num): # for mini x axis
                for l in range(0, num): # for mini y axis
                    rgb = imAr[j + k][i + l]
                    RGBvalsInSquare.append(rgb)  # should be 81 long
            squareList[int(j / num)][int(i / num)] = getAvgRGB(RGBvalsInSquare) # img reconstruction is backwards (height, then width)
    return np.asarray(squareList)

def constructNewImg(img, divSize):
    pixelAr = getNewPixelAr(img, divSize)

    newImg = Image.new('RGB', img.size)
    for i in range(0, int(pixelAr.shape[1])):
        for j in range(0, pixelAr.shape[0]):
            tempImg = img
            tempImg = tempImg.resize((divSize, divSize))
            layer = Image.new('RGB', tempImg.size, (pixelAr[j][i][0], pixelAr[j][i][1], pixelAr[j][i][2]))
            tempImg = Image.blend(tempImg, layer, .5)
            newImg.paste(tempImg, (divSize * i, divSize * j))
    return newImg


# construct the new image from the new array, using the width and height of the original image to resize
# kinda useless, but sorta cool
def constructLowerQualityIm(oldImAr, newImAr):
    newImg = Image.fromarray(newImAr.astype(np.uint8))
    width = oldImAr.shape[1]
    height = oldImAr.shape[0]
    newImg = newImg.resize((width, height))
    return newImg

#combine all the functions above and run it in standard format
def lowerImgQuality(imgPath, divSize):
    im = Image.open(imgPath)
    originalPixelAr = np.asarray(im)
    im.show()

    newImg = constructNewImg(im, divSize)
    newImg = newImg.resize((originalPixelAr.shape[1], originalPixelAr.shape[0]))
    newImg.save('newImg.jpg')
    newImg.show()



def main():
    lowerImgQuality('image0.jpg', 10)

main()