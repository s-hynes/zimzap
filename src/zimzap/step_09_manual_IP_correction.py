"""This module contains step 9, manual instrumental polarisation correction."""
import numpy as np
from photutils.aperture import ApertureStats, CircularAnnulus
from astropy.io import fits
import datetime as dt

c_x, c_y = 255.75, 255.5

def inst_pol(diff_im, int_im, Rin, Rout):
    """
    
    **Inputs:**
    
    `diff_im`: double difference image
    
    `Int_im`: intensity image
    
    `Rin`: inner radius of the annulus used for instrumental
    polarisation correction

    `Rout`: outer radius of the annulus used for instrumental
    polarisation correction

    **Outputs:**

    `IP_corrected`:
    """

    deg_pol = diff_im / int_im
    c_x, c_y = 255.75, 255.5

    aper = CircularAnnulus( (c_x, c_y), Rin, Rout)
    aperstats = ApertureStats(deg_pol, aper)
    median = aperstats.median

    IP_corrected = diff_im - median * int_im

    return IP_corrected

def fix(diff_im, Rin, Rout):
    """This step needs to be performed so that the background is zero before 
    calculating Qphi and Uphi"""

    c_x, c_y = 255.75, 255.5

    aper = CircularAnnulus( (c_x, c_y), Rin, Rout)
    aperstats = ApertureStats(diff_im, aper)
    median = aperstats.median

    fixed = diff_im - median

    return fixed