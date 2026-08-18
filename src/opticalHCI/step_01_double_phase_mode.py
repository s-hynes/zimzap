"""This module contains step 1, splitting the raw data cube into the two 
components of the double phase mode."""
from astropy.io import fits

def double_phase_mode(filename, detector:str):
    """This function splits the images from a .fits data cube into 0 and 
    pi phase mode cubes.
    
    It returns a tuple where the 1st element is the 0 data cube and the 
    2nd is the pi data cube
    
    ## **Input parameters:**

    **`filename`**: Name of the .fits file to be split.
    
    **`detector`**: Name of the detector that the images are taken from.
    
    ## **Outputs:**
    
    **0 -`image_data_0`**:  Data from the file that was recorded in the 
                            zero phase mode
    
    **1 -`image_data_pi`**: Data from the file that was recorded in the 
                            pi phase mode"""

    hdul = fits.open(filename)

    if detector=="Callas":
        image_data = hdul[1].data
    elif detector=="Bartoli":
        image_data = hdul[2].data
    else:
        raise Exception("""Invalid detector entered. Detector must be 
                        \"Callas\" or \"Bartoli\".""")

    hdul.close()
    image_data_0    = image_data[::2,  :, :]
    image_data_pi   = image_data[1::2, :, :]

    return image_data_0, image_data_pi