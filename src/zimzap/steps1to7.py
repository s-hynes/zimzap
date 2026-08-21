"""This script performs steps 1 through 7 in the data reduction."""
from .step_01_double_phase_mode import double_phase_mode
from .step_02_bias_subtraction import overscan
from .step_03_separating_rows import separate_rows
from .step_04_centring import *
from .step_05_single_difference import single_diff_pol, intensity
from .step_06_removing_dither import dedither
from .step_07_binning_pixels import binning
from astropy.io import fits
import numpy as np
import datetime as dt
from .inputs import save_fits, save_steps, saving_dir, dir_in_str
import time

def steps1to7(data_dir:str, file:str, save_dir:str, detector:str, Stokes, 
              first_cycle:bool, centre_one_cycle:bool, time_and_log=False): 
    """Performs steps 1 to 7 in the data reduction.""" 

    # Step 1: Double phase mode

    doub_ph_start_time = time.monotonic()

    zero    = double_phase_mode(data_dir + "/" + file, detector)[0]
    pi      = double_phase_mode(data_dir + "/" + file, detector)[1]

    doub_ph_finish_time = time.monotonic()
    time_taken_doub_ph = doub_ph_finish_time - doub_ph_start_time

    # Step 2: Removing overscan and bias subtraction

    oversc_start_time = time.monotonic()

    zero_no_overscan = overscan(zero)
    pi_no_overscan   = overscan(pi)

    oversc_finish_time = time.monotonic()
    time_taken_oversc = oversc_start_time - oversc_finish_time

    # Step 3: Separating rows of orthogonal polarisation directions

    sep_rows_start_time = time.monotonic()

    ord_0 = separate_rows(zero_no_overscan, phase="0")[0]
    ext_0 = separate_rows(zero_no_overscan, phase="0")[1]

    ord_pi = separate_rows(pi_no_overscan, phase="pi")[0]
    ext_pi = separate_rows(pi_no_overscan, phase="pi")[1]

    sep_rows_finish_time = time.monotonic()
    time_taken_sep_rows = sep_rows_finish_time - sep_rows_start_time

    # Step 4: Centring star using Gaussian fit

    centring_start_time = time.monotonic()

    if centre_one_cycle:

        ord_0   = dedither(ord_0, data_dir + "/" + file)
        ext_0   = dedither(ext_0, data_dir + "/" + file)
        ord_pi  = dedither(ord_pi, data_dir + "/" + file)
        ext_pi  = dedither(ext_pi, data_dir + "/" + file)

        if first_cycle:
            ord_0_star_coords = star_coords(ord_0[0])
            ext_0_star_coords = star_coords(ext_0[0])
            ord_pi_star_coords = star_coords(ord_pi[0])
            ext_pi_star_coords = star_coords(ext_pi[0])
            
            ord_0_centred   = centre_star_with_coordinates(ord_0, ord_0_star_coords)
            ext_0_centred   = centre_star_with_coordinates(ext_0, ext_0_star_coords)
            ord_pi_centred  = centre_star_with_coordinates(ord_pi, ord_pi_star_coords)
            ext_pi_centred  = centre_star_with_coordinates(ext_pi, ext_pi_star_coords)
        else:
            ord_0_centred   = centre_star_with_coordinates(ord_0, ord_0_star_coords)
            ext_0_centred   = centre_star_with_coordinates(ext_0, ext_0_star_coords)
            ord_pi_centred  = centre_star_with_coordinates(ord_pi, ord_pi_star_coords)
            ext_pi_centred  = centre_star_with_coordinates(ext_pi, ext_pi_star_coords)
    else:
        ord_0_centred   = centre_star(ord_0)
        ext_0_centred   = centre_star(ext_0)
        ord_pi_centred  = centre_star(ord_pi)
        ext_pi_centred  = centre_star(ext_pi)

    centring_finish_time = time.monotonic()
    time_taken_centring = centring_finish_time - centring_start_time

    # Step 5: Single difference

    sing_diff_start_time = time.monotonic()

    sing_diff_rectangular = single_diff_pol(ord_0_centred, ord_pi_centred, ext_0_centred, ext_pi_centred)
    int_rectangular = intensity(ord_0_centred, ord_pi_centred, ext_0_centred, ext_pi_centred)

    sing_diff_finish_time = time.monotonic()
    time_taken_sing_diff = sing_diff_finish_time - sing_diff_start_time

    # Step 7: Binning pixels

    binning_start_time = time.monotonic()

    if detector=="Callas":
        sing_diff_square = np.rot90(np.flipud(binning(sing_diff_rectangular)), k=1)
        int_square = np.rot90(np.flipud(binning(int_rectangular)), k=1)
    elif detector=="Bartoli":
        sing_diff_square = np.rot90(binning(sing_diff_rectangular), k=2)
        int_square = np.rot90(binning(int_rectangular), k=2)    

    binning_finish_time = time.monotonic()
    time_taken_binning = binning_finish_time - binning_start_time

    if time_and_log:
        print(f"# Step 1 (double phase mode) took "\
            f"{time_taken_doub_ph} s")
        print(f"# Step 2 (overscan removal and bias subtraction) took "\
            f"{time_taken_doub_ph} s")
        print(f"# Step 3 (separating rows) took "\
            f"{time_taken_sep_rows} s")
        print(f"# Step 4 (centring star using Gaussian fit) took "\
            f"{time_taken_centring} s")
        print(f"# Step 5 (single difference) took "\
            f"{time_taken_sing_diff} s")
        print(f"# Step 7 (binning pixels) took "\
            f"{time_taken_binning} s")
        print("#"+79*"-")

    return sing_diff_square, int_square

if __name__=="__main__":
    start_time = time.monotonic()
    print("\nScript started at: ", time.ctime())

    data_dir = dir_in_str
    save_dir = saving_dir
    filename = "SPHER.2016-03-31T04_06_44.299.fits"

    hdul = fits.open( data_dir + "/" + filename)
    Stokes = hdul[0].header['HIERARCH ESO OCS3 ZIMPOL POL STOKES']
    hdul.close()
    print("\nStokes = {0}\n".format(Stokes))

    steps1to7(data_dir, filename, save_dir, "Callas", Stokes, first_cycle=True)
    
    end_time = time.monotonic()
    print("\nTime taken: ", dt.timedelta(seconds=end_time - start_time))
    print("\nScript finished at: \n", time.ctime())