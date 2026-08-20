import numpy as np
from photutils.aperture import CircularAperture, ApertureStats, CircularAnnulus
import matplotlib.pyplot as plt
from astropy.io import fits
import datetime as dt

hdu_list_tot_int = fits.open('C:/Users/Stephen/OneDrive - National University of Ireland, Galway/24-25 FYP/Data/manipulated-data/steps_presentation/2025-03-25-Callas-35-total_intensity_average.fits')
image_tot_int = hdu_list_tot_int[0].data
hdu_list_tot_int.close()

hdu_list_pol_int = fits.open('C:/Users/Stephen/OneDrive - National University of Ireland, Galway/24-25 FYP/Data/manipulated-data/steps_presentation/2025-03-25-Callas-36-polarised_intensity_average.fits')
image_pol_int = hdu_list_pol_int[0].data
hdu_list_pol_int.close()

c_x, c_y = 255.75, 255.5

aper1 = CircularAnnulus( (c_x, c_y), 6, 7.5)
#aper2 = CircularAnnulus( (c_x, c_y), 200, 250)

plt.figure(1)
plt.imshow(image_tot_int, origin ='lower', cmap='hot', norm='symlog')
# I added this line to show the circle, to make sure that I'm putting it in the right place.
aper1.plot(color='green', lw = 1);
#aper2.plot(color='blue', lw = 1);
plt.colorbar()

plt.figure(2)
plt.imshow(image_pol_int, origin ='lower', cmap='hot', norm='symlog')
aper1.plot(color='green', lw = 1);
plt.colorbar()
plt.show()