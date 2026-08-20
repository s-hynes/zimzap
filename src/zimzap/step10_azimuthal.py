import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import datetime as dt
from .step_09_manual_IP_correction import inst_pol

def azimuthal(Q_val, U_val):
    
    phi = np.zeros_like(Q_val)
    
    for i in range(phi.shape[0]):
        for j in range((phi.shape[1])):
            # i corresponds to y, j corresponds to x
            phi[i,j] = np.arctan( (255.75 - j)/(i - 255.5))

    Q_phi = -Q_val * np.cos(2*phi) - U_val * np.sin(2*phi)
    U_phi = +Q_val * np.sin(2*phi) - U_val * np.cos(2*phi)

    return Q_phi, U_phi