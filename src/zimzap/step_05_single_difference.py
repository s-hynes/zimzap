"""This module contains step 5, creating single difference polarisation 
and intensity images."""
import numpy as np

def single_diff_pol(o_0, o_pi, e_0, e_pi):
    """Creates single difference polarisation image.
    
    **Inputs:**

    `o_0`: The ordinary ray image in the zero phase mode

    `o_pi`: The ordinary ray image in the pi phase mode

    `e_0`: The extraordinary ray image in the zero phase mode

    `e_pi`: The extraordinary ray image in the pi phase mode

    **Outputs:**
    
    `sing_diff_pol`: The single difference polarisation image"""
    
    o_0_avg = np.average(o_0, axis=0)
    o_pi_avg = np.average(o_pi, axis=0)
    e_0_avg = np.average(e_0, axis=0)
    e_pi_avg = np.average(e_pi, axis=0)

    Q_zero = o_0_avg - e_0_avg
    Q_pi = o_pi_avg - e_pi_avg

    sing_diff_pol = (1/2)*(Q_zero - Q_pi)

    return sing_diff_pol

def intensity(o_0, o_pi, e_0, e_pi):
    """Creates single difference intensity image.
    
    **Inputs:**

    `o_0`: The ordinary ray image in the zero phase mode

    `o_pi`: The ordinary ray image in the pi phase mode

    `e_0`: The extraordinary ray image in the zero phase mode

    `e_pi`: The extraordinary ray image in the pi phase mode

    **Outputs:**
    
    `I`: The single difference intensity image"""

    o_0_avg = np.average(o_0, axis=0)
    o_pi_avg = np.average(o_pi, axis=0)
    e_0_avg = np.average(e_0, axis=0)
    e_pi_avg = np.average(e_pi, axis=0)

    I = (1/2)*(o_0_avg + o_pi_avg + e_0_avg + e_pi_avg)

    return I

if __name__ == "__main__":
    pass