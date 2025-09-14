import cv2 as cv
import numpy as np
IMAGE_SIZE = 28

# Functions to preprocess images, preparing them for use in an image classification task.

def preprocess_test_image(path): # This function processes images from the test dataset.
    grey_image = cv.imread(path, cv.IMREAD_GRAYSCALE)
    binary_image = cv.threshold(grey_image, 120, 255, cv.THRESH_BINARY)[1] # Converts the grayscale image to binary using a higher threshold of 120.
                                                                           # pixel values above 120 become white (255), and everything else becomes black (0).
    dilation_image = cv.erode(binary_image, kernel=np.ones((5,5),np.uint8), iterations = 5) # Erosion reduces the white areas.
                                                                                           # (The pixel will only remain white if all the pixels in the neighborhood defined by the kernel are also white.)
    resized_image = cv.resize(dilation_image, (IMAGE_SIZE, IMAGE_SIZE))
    dilation_image = cv.erode(resized_image, kernel=np.ones((3,3),np.uint8), iterations = 1)
    dilation_image[dilation_image!=255] = 0 # If a pixel is not 255 (meaning it is not white), the corresponding value in the mask is True.
                                            # Then the pixel is set to 0 (black).
    dilation_image[dilation_image==255] = 1
    print('size of resized test image: ', resized_image.shape)
    return dilation_image

def preprocess_training_images(path): # This function is very similar to the preprocess_test_image function, 
                                      # but it's used for preprocessing training images.
    image = cv.imread(path, cv.IMREAD_GRAYSCALE)
    binary_image = cv.threshold(image, 180, 255, cv.THRESH_BINARY)[1]
    dilation_image = cv.erode(binary_image, kernel=np.ones((3,3),np.uint8), iterations = 1)
    dilation_image[dilation_image!=255] = 0
    dilation_image[dilation_image==255] = 1
    return dilation_image

