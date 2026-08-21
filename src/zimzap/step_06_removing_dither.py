"""This script carries out step 6, removing dithering from the images. 
This step isn't currently used in the pipeline because centring the star 
using a Gaussian fit also removes the dither. I will retain the code for 
the time being (18/06/2026)."""
from astropy.io import fits
import scipy.ndimage 
import numpy as np

def dedither(img, fits_file:str):
    """Removes dithering from image.
    
    **Input:**

    `img`: The input image

    `fits_file`: The name of the fits file that the raw data came from.

    **Output:**

    `shifted_img`: The image with dithering removed.
    """

    hdul = fits.open(fits_file)

    # These lines find the x and y values for dithering in the fits file.
    x_shift = hdul[0].header['HIERARCH ESO INS3 POS4 POS']
    y_shift = hdul[0].header['HIERARCH ESO INS3 POS4 POS'] 
    hdul.close()

    # I have a feeling this could break if we're not dealing with cubes.
    m = img.shape[0]
    shifted_img = np.zeros_like(img)
    for i in range(m):
        shifted_img[i,:,:] = scipy.ndimage.shift(img[i,:,:], [y_shift/2, x_shift])

    # In Christian's IRDIS pipeline: 
    # x_shift = [1024-1]/2 - x_star - x_dith
    # x_dith = hdul[0].header['HIERARCH ESO INS3 POS3 POS']

    return shifted_img

if __name__ == "__main__":
    pass