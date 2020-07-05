# Image Fractalizer
Image Fractalizer is a program in which you can input any JPG/JPEG/PNG image, and then reconstruct that same image from many smaller, filtered copies of itself.

## Examples

### Concert Hall
- Original Image
![Unfract Concert Example](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/Ex1UnFract.jpeg)

- Fractalized Image with a Division Size of 20
![Fract Concert Example](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/Ex1Fract20.jpeg)

### Lake
- Original Image
![Unfract Lake Example](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/Ex2FUnFract.png)

- Fractalized Image with a Division Size of 20 (You might need to zoom in to see the factalization on this image)
![Fract Lake Example](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/Ex2Fract20.png)

## How it Works
The algorithm to reconstruct the picture out of copies of itself is relatively simple and straightforward:
1. The image is resized slightly so that both dimensions are multiple of the inputted division size (which is explained in greater detail below).
2. The image is traversed by going across the length and width of the image, skipping a number of pixels equal to the Div. Size on each iteration.
This effectively "carves out" many small squares of size Div. Size x Div. Size within the original image. For the current small square that is being
"carved out" of the image, traverse all of its pixels and store their RGB contents
3. Find the average RGB value of all pixels in this small square and store it
4. Repeat steps 2 and 3 until all pixels have been traversed 
5. Create a new, blank image the size of the resized inputted image. For each pixel in the newly created array, create shrunk copy of the original image,
and then apply a filter based on the RGB data in the current pixel. Place this shrunk, filtered, image at the appropriate location in on the new picture,
and repeat until all pixels in the the pixel array have been traversed
6. Resize the newly-created image so that it matches the dimension of the origional image as it was inputted

## Division Size Explanation
The best way to show exactly how the division size works is simply by showing examples.

- Here is a standard image of a dog:
![Original Dog](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/Dog.jpeg)

- Here's the image put through the fractalizer with a division size of 150:
  - As you can see, it's very difficult to see how these images reconstruct the original image 
![150 Dog](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/DogFract150.jpeg)

- Here is the image with a division size of 100
![100 Dog](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/DogFract100.jpeg)

- A division size of 50
![50 Dog](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/DogFract50.jpeg)

- And a division size of 10
![10 Dog](https://github.com/robbiehammond/Image-Fractalizer/blob/master/TestImages/DogFract10.jpeg)

As can be seen, the smaller the division size, the greater total copies of the image are used to reconstruct the image, leading to less approximation and
greater detail. So a division size of 1 would yield a 1:1 ratio between the amount of pixels in the original image and the amount of image copies placed
on the new image. This greater detail does come at a cost - the more images need to be filtered and added the reconstruction, the more processing power
and time it takes the fractalizer to run. Depending on the image dimensions and division size, the fractalizer took anywhere from 5 seconds to 5 minutes to
complete on an i7-4790k for reasonably sized images and division sizes. The GUI does have a progress bar, so you are able to see the rate at which the fractalizer
is running on your hardware.

## Download Instructions 
I'll add these later 