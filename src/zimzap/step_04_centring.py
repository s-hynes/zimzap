"""
This module contains step 4, centring the star in the image. It uses a 
2D Gaussian fit to find the location of the most intense pixel in the 
image and then shifts the image so that this pixel is at the centre of 
the image.
This code was originally written by Cian Mulkern then modified to be 
used with this pipeline.

@author: Cjmul
"""
from .step_01_double_phase_mode import double_phase_mode
from .step_02_bias_subtraction import overscan
from .step_03_separating_rows import separate_rows
from astropy.io import fits
import numpy as np
import os
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
import scipy
import time

def star_coords(image, x_dith=0, y_dith=0, print_coords=False):

    # Cuts out the point source from the data
    ps = image[:,206:-306]

    # Finds the max value of array that contains the point source
    maxval = np.array(ps).ravel()[np.argmax(ps)]

    # Finds the coordinates of this max value
    coords = np.unravel_index(np.argmax(ps), shape = np.array(ps).shape)

    # Defines Levenberg-Marquardt least squares fit
    fitter = fitting.LevMarLSQFitter()

    # Applies fitter
    y_shape = np.shape(ps)[1]
    x_shape = np.shape(ps)[0]
    y,x = np.mgrid[:y_shape,:x_shape]
    z = ps
    p_init = models.Gaussian2D(amplitude =maxval, x_mean=coords[1], y_mean=coords[0], x_stddev=4, y_stddev=4, theta=None)
    p = fitter(p_init, x, y, z)

    star_x_coords_dithered = p.x_mean[0] + 206
    star_y_coords_dithered = p.y_mean[0]

    if print_coords:
        # Debugging line, checking how much the star position changes
        print(f"Star position: ({star_x_coords_dithered+x_dith}, {star_y_coords_dithered+y_dith/2})")

    return star_x_coords_dithered, star_y_coords_dithered

def centre_star(image, x_dith=0, y_dith=0, print_coords=False):

    m = image.shape[0]
    centred_star = np.zeros_like(image)
    for i in range(m):

        x_coords, y_coords = star_coords(image[i,:,:], print_coords=print_coords)

        # Using location of most intensity in Gaussian fit to centre star.
        x_shift = 511.5 - x_coords
        y_shift = 255.5 - y_coords
        centred_star[i,:,:] = scipy.ndimage.shift(image[i,:,:], [y_shift, x_shift])

        # Debugging line, checking how much the star position changes
        # print(f"Star position: ({p.x_mean[0]+x_dith}, {p.y_mean[0]+y_dith/2})")
    
    return centred_star

def centre_star_with_coordinates(image, star_coords:tuple, print_coords=False):

    m = image.shape[0]
    centred_star = np.zeros_like(image)
    for i in range(m):

        x_coords, y_coords = star_coords

        # Using location of most intensity in Gaussian fit to centre star.
        x_shift = 511.5 - x_coords
        y_shift = 255.5 - y_coords
        centred_star[i,:,:] = scipy.ndimage.shift(image[i,:,:], [y_shift, x_shift])
    
    return centred_star

def undither_and_centre(fits_file, image, star_coords,\
                        print_coords=False):

    m = image.shape[0]
    centred_star = np.zeros_like(image)

    hdul = fits.open(fits_file)
    # These lines find the x and y values for dithering in the fits file.
    x_dither = hdul[0].header['HIERARCH ESO INS3 POS4 POS']
    y_dither = hdul[0].header['HIERARCH ESO INS3 POS4 POS'] 
    hdul.close()

    for i in range(m):

        undithered_image = scipy.ndimage.shift(image[i,:,:], [y_dither/2, x_dither])

        #x_coords, y_coords = star_coords(image[i,:,:], print_coords=print_coords)

        # Using location of most intensity in Gaussian fit to centre star.
        x_shift = 511.5 - star_coords[0]
        y_shift = 255.5 - star_coords[1]
        centred_star[i,:,:] = scipy.ndimage.shift(undithered_image[:,:], [y_shift, x_shift])

        # Debugging line, checking how much the star position changes
        # print(f"Star position: ({p.x_mean[0]+x_dith}, {p.y_mean[0]+y_dith/2})")
    
    return centred_star

"""The centering of the star seems to take ages for some reason. 
Update 06/03/2025: I think it takes ages because with the current setup, 
it centres 8x120=960 images for the test data set."""

if __name__ == '__main__':
    
    dir_in_str = """C:/Users/Stephen/Documents/FYP_Pipeline_Local/test_working_directories/small_dataset/raw"""
    saving_dir = """C:/Users/Stephen/OneDrive - National University of Ireland, 
    Galway/24-25 FYP/project-code/manipulated-data/step7/fixing-butterfly"""

    print("\nScript started at: "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    
    k = 0
    for file in os.scandir(dir_in_str):
        #filename = os.fsdecode(file)
        filename = file.name
        if filename.endswith(".fits"):
            file_path = os.path.join(dir_in_str, filename)
            hdul = fits.open(file_path)
            x_dither = hdul[0].header['HIERARCH ESO INS3 POS4 POS']
            y_dither = hdul[0].header['HIERARCH ESO INS3 POS4 POS'] 
            hdul.close()

            zero = double_phase_mode(file_path, "Callas")[0]
            pi   = double_phase_mode(file_path, "Callas")[1]
            zero_no_overscan = overscan(zero)
            pi_no_overscan   = overscan(pi)

            ord_0 = separate_rows(zero_no_overscan, phase="0")[0]
            ext_0 = separate_rows(zero_no_overscan, phase="0")[1]
            ord_pi = separate_rows(pi_no_overscan, phase="pi")[0]
            ext_pi = separate_rows(pi_no_overscan, phase="pi")[1]

            print(ord_0.shape)

            k += int(1)
            print(f"\nProcessing up to centering of star done for FITS file #{k}: "\
                  f"{filename}")

            centring_start_time = time.monotonic()

            ord_0_star_coords = star_coords(ord_0[0])
            ext_0_star_coords = star_coords(ext_0[0])
            ord_pi_star_coords = star_coords(ord_pi[0])
            ext_pi_star_coords = star_coords(ext_pi[0])

            ord_0_centred   = undither_and_centre(file_path, ord_0, ord_0_star_coords)
            ext_0_centred   = undither_and_centre(file_path, ext_0, ext_0_star_coords)
            ord_pi_centred  = undither_and_centre(file_path, ord_pi, ord_pi_star_coords)
            ext_pi_centred  = undither_and_centre(file_path, ext_pi, ext_pi_star_coords)

            centring_finish_time = time.monotonic()
            centring_time_taken = centring_finish_time - centring_start_time

            print(f"Centering of star done for FITS file #{k}. "\
                  f"Time taken: {centring_time_taken:20} s")

            """
            ord_0_centred   = centre_star(ord_0)
            print("Ordinary 0 centred for image {0}.".format(k))
            ext_0_centred   = centre_star(ext_0)
            print("Extraordinary 0 centred for image {0}.".format(k))
            ord_pi_centred  = centre_star(ord_pi)
            print("Ordinary pi centred for image {0}.".format(k))
            ext_pi_centred  = centre_star(ext_pi)
            print("Extraordinary pi centred for image {0}.".format(k))
            print("Shapes: ",ord_0_centred.shape,ext_0_centred.shape,ord_pi_centred.shape,ext_pi_centred.shape)
            print(100*"-")"""

    print("\nScript finished at: "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")