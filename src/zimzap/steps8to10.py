from .step_08_double_difference import double_diff
from .step_09_manual_IP_correction import inst_pol, fix
from .step10_azimuthal import azimuthal
from astropy.io import fits
import datetime as dt
import time
import numpy as np
import os
from .inputs import save_fits, save_steps, dir_in_str, saving_dir

def check_directories():
    """This function checks checks for the existence of the directory for raw 
    FITS files and the directories where the final reduced data are saved. If 
    any of these don't exist, this function creates them."""
    
    raw_data_dir = os.path.join(os.getcwd(), "raw")
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
        print(f"""\nThe raw data directory {raw_data_dir} did not exist. It was 
    created but you now need to put your raw FITS files in there.""")

    for reduction_stage in ["star_pol_subtr", "no_star_pol_subtr"]:
        for detector in ["Callas", "Bartoli", "detectors_combined"]:
            path_1 = os.path.join(os.getcwd(), f"reduced_pdi/{reduction_stage}/{dt.date.today()}/{detector}/")
            if not os.path.exists(path_1):
                os.makedirs(path_1)

# Radii for manual IP correction annulus
r_in, r_out = 6, 7.5

def combine(save_dir:str, Callas_image, Bartoli_image, savesteps=False):

    Callas_image_rotated = np.rot90(Callas_image, k=3).reshape(1,512,512)
    Bartoli_image = Bartoli_image.reshape(1,512,512)

    images_combined = np.average( np.append(Callas_image_rotated, Bartoli_image, axis=0), axis=0)

    return images_combined

# This function needs a more descriptive name
def itsready(data_dir:str, save_dir:str, detector:str, savesteps=False):

    #hdu_array = double_diff(data_dir, save_dir, detector, savesteps=save_steps)
    #Q_im, U_im, Int_Q, Int_U = hdu_array[0:4]

    print("\n"+80*"#")
    print(f"# Starting steps 1 to 8 of data reduction for {detector}. Step 8 "\
          "computes double difference and double sum images "\
            f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print(80*"#"+"\n")
    start_time_1_to_8 = time.monotonic()

    Q_im, U_im, Int_Q, Int_U, Int_tot, Pol_int = double_diff(data_dir, save_dir, detector, savesteps=save_steps)

    end_time_1_to_8 = time.monotonic()
    print("\n"+80*"#")
    print(f"# Double difference and double sum images computed for {detector} "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print("# Time taken: ", dt.timedelta(seconds=end_time_1_to_8 - start_time_1_to_8))
    print(80*"#")

    ###########################################################################
    # Saving images prior to instrumental polarisation correction
    ###########################################################################

    data_dict = {"_Q": Q_im, "_U": U_im, "_I_Q": Int_Q, "_I_U": Int_U,
        "_I_tot": Int_tot, "_I_pol": Pol_int}

    for key, value in data_dict.items():
        hdu = fits.PrimaryHDU(data=value)
        hdu.writeto(os.path.join(os.getcwd(), f"reduced_pdi/no_star_pol_subtr/{dt.date.today()}/{detector}/{key}.fits"), overwrite=True)

    ###########################################################################
    # Carrying out instrumental polarisation correction and computing azimuthal
    # Stokes parameters
    ###########################################################################

    print("\n"+80*"#")
    print("# Carrying out manual instrumental polarisation correction "\
          f"for {detector} "\
            f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print(80*"#")
    start_time_9 = time.monotonic()

    Q_im_IPcorr = fix(inst_pol(Q_im, Int_Q, Rin=6, Rout=7.5), Rin=100, Rout=200)
    U_im_IPcorr = fix(inst_pol(U_im, Int_U, Rin=6, Rout=7.5), Rin=100, Rout=200)


    PolInt = np.sqrt( Q_im_IPcorr**2 + U_im_IPcorr**2)

    end_time_9 = time.monotonic()
    print("\n"+80*"#")
    print("# Manual instrumental polarisation correction complete for "\
          f"{detector} "\
            f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print("# Time taken: ", dt.timedelta(seconds=end_time_9 - start_time_9))
    print(80*"#")

    print("\n"+80*"#")
    print(f"# Computing azimuthal Stokes parameters for {detector} "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print(80*"#")
    start_time_10 = time.monotonic()

    Q_phi, U_phi = azimuthal(Q_im_IPcorr, U_im_IPcorr)

    end_time_10 = time.monotonic()
    print("\n"+80*"#")
    print("# Azimuthal Stokes parameters have been computed for "\
          f"{detector} "\
            f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print("# Time taken: ", dt.timedelta(seconds=end_time_10 - start_time_10))
    print(80*"#")

    ###########################################################################
    # Saving images after instrumental polarisation correction
    ###########################################################################

    #data_dict["_Q_phi"] = Q_phi
    #data_dict["_U_phi"] = U_phi
    
    data_dict = {"_Q": Q_im_IPcorr, "_U": U_im_IPcorr, "_I_pol": PolInt, 
                 "_Q_phi": Q_phi, "_U_phi": U_phi}

    for key, value in data_dict.items():
        hdu = fits.PrimaryHDU(data=value)
        hdu.writeto(os.path.join(os.getcwd(), f"reduced_pdi/star_pol_subtr/{dt.date.today()}/{detector}/{key}_star_pol_subtr.fits"), overwrite=True)

    return Q_im_IPcorr, U_im_IPcorr, PolInt, Q_phi, U_phi

def final_combination(data_dir:str, savesteps=False):

    raw_data_dir = os.path.join(os.getcwd(), "raw")

    Callas_images = itsready(raw_data_dir, saving_dir, "Callas", savesteps=save_steps)
    Bartoli_images = itsready(raw_data_dir, saving_dir, "Bartoli", savesteps=save_steps)

    print("\n"+80*"#")
    print(f"# Combining images from Callas and Bartoli "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print(80*"#")
    start_time_comb = time.monotonic()

    Q_IP_corr_combined = combine(saving_dir, Callas_images[0], Bartoli_images[0], savesteps=save_steps)
    U_IP_corr_combined = combine(saving_dir, Callas_images[1], Bartoli_images[1], savesteps=save_steps)
    PolInt_combined = combine(saving_dir, Callas_images[2], Bartoli_images[2], savesteps=save_steps)
    Q_phi_combined = combine(saving_dir, Callas_images[3], Bartoli_images[3], savesteps=save_steps)
    U_phi_combined = combine(saving_dir, Callas_images[4], Bartoli_images[4], savesteps=save_steps)

    end_time_comb = time.monotonic()
    print("\n"+80*"#")
    print("# Images from Callas and Bartoli have been combined "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print("# Time taken: ", dt.timedelta(seconds=end_time_comb - start_time_comb))
    print(80*"#")

    data_dict = {"_Q": Q_IP_corr_combined, "_U": U_IP_corr_combined, 
                 "_I_pol": PolInt_combined, "_Q_phi": Q_phi_combined, 
                 "_U_phi": U_phi_combined}

    for key, value in data_dict.items():
        hdu = fits.PrimaryHDU(data=value)
        hdu.writeto(os.path.join(os.getcwd(), f"reduced_pdi/star_pol_subtr/{dt.date.today()}/detectors_combined/{key}_star_pol_subtr.fits"), overwrite=True)

if __name__=="__main__":

    print("\nScript started at: "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    start_time = time.monotonic()

    raw_data_dir = os.path.join(os.getcwd(), "raw")
    check_directories()
    final_combination(raw_data_dir)

    end_time = time.monotonic()
    print("\nScript finished at: "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print("\nTime taken: ", dt.timedelta(seconds=end_time - start_time))