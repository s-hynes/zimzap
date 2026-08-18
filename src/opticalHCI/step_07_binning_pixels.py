"""This module contains step 7, binning pixels in the x-direction to 
recover even dimensions in x and y."""
import numpy as np

def binning(img):
    """Takes a 1024x512 pixel image and bins pixels in the x-direction 
    to create a 512x512 image (i.e. one with even dimensions in x and 
    y).
    
    **Input:**
    
    `img`: The input 1024x512 image

    **Output:**
    
    `square_img`: The binned 512x512 image
    """

    """
    Y is the y dimension of the image. In ZIMPOL's case, 512 pixels.
    M is the size of the image array. In this case, 
    512 x 1024 = 524,288 = 2^19"""
    Y = img.shape[0]
    M = img.size

    """
    arr2 is a 2D array with 262,144 rows and 2 columns. Each row is a 
    pair of horizontally adjacent pixel values.
    arr3 is a 1D array of length 262,144 where the value for each of 
    these pixel pairs has been averaged.
    arr3 is then reshaped to give the final 512 x 512 image, called 
    square_img."""
    arr2 = img.reshape((M//2, 2))
    arr3 = np.mean(arr2, axis=1)
    square_img = arr3.reshape( (arr3.size)//Y,Y)

    return square_img

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    y = 2**4
    x = 2*y

    array = np.arange(1, x*y + 1).reshape(y, x)
    array2 = binning(array)

    plt.figure(1)
    plt.title("Example \"Toy\" Image Before Binning Pixels")
    plt.imshow(array,origin ='lower', cmap='plasma')
    plt.colorbar()

    plt.figure(2)
    plt.title("Example \"Toy\" Image After Binning Pixels")
    plt.imshow(array2,origin ='lower', cmap='plasma')
    plt.colorbar()
    plt.show()