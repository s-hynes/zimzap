"""This module contains step 8, creating double difference images."""
import numpy as np
import os
from astropy.io import fits
from .steps1to7 import steps1to7
import datetime as dt
import time
from datetime import timedelta
from .inputs import save_fits, save_steps, saving_dir, dir_in_str

def double_diff(data_dir:str, save_dir:str, detector:str, savesteps=False):
    """Carries out the processing for double difference images.
    
    **Input parameters:**

    `data_dir`: The directory that the raw data is in

    `save_dir`: The directory that the processed images from the data
    reduction will be saved in

    `detector`: Name of the detector that the images are taken from.
    
    `savesteps`: Whether or not intermediate steps in the data reduction 
    will be saved. Default value is `False`.


    **Outputs:**
    Outputs a tuple containing the following values:

    0 -`Q_val_ave`:         Q double difference image

    1 -`U_val_ave`:         U double difference image

    2 -`Int_Q_ave`:         Q intensity image

    3 -`Int_U_ave`:         U intensity image

    4 -`Int_tot_ave`:       Total intensity image

    5 -`Pol_int_ave`:       Polarised intensity image
    """

    Qplus   = 0 
    Qminus  = 0
    Uplus   = 0
    Uminus  = 0
    n_cycles = 0

    start_time_sing_diff = time.monotonic()

    for file in os.scandir(data_dir):
        #filename = os.fsdecode(file)
        filename = file.name
        if filename.endswith(".fits"):

            hdul = fits.open( data_dir + "/" + filename)
            Stokes = hdul[0].header['HIERARCH ESO OCS3 ZIMPOL POL STOKES']
            hdul.close()

            if Stokes == "Qplus":
                if Qplus == 0:
                    Qplus_singdiff_cyc = steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512)
                    Qplus_int_cyc = steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512)
                else:
                    Qplus_singdiff_cyc  = np.append(Qplus_singdiff_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512), axis=0)
                    Qplus_int_cyc       = np.append(Qplus_int_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512), axis=0)
                Qplus += 1
            elif Stokes == "Qminus":
                if Qminus == 0:
                    Qminus_singdiff_cyc = steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512)
                    Qminus_int_cyc      = steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512)
                else: 
                    Qminus_singdiff_cyc = np.append(Qminus_singdiff_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512), axis=0)
                    Qminus_int_cyc      = np.append(Qminus_int_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512), axis=0)
                Qminus += 1              
            elif Stokes == "Uplus":
                if Uplus == 0:
                    Uplus_singdiff_cyc  = steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512)
                    Uplus_int_cyc       = steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512)
                else:
                    Uplus_singdiff_cyc  = np.append(Uplus_singdiff_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512), axis=0)
                    Uplus_int_cyc       = np.append(Uplus_int_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512), axis=0)  
                Uplus += 1
            elif Stokes == "Uminus":
                if Uminus == 0:
                    Uminus_singdiff_cyc = steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512)
                    Uminus_int_cyc      = steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512)
                else:
                    Uminus_singdiff_cyc = np.append(Uminus_singdiff_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[0].reshape(1,512,512), axis=0)
                    Uminus_int_cyc      = np.append(Uminus_int_cyc, steps1to7(data_dir, filename, save_dir, detector, Stokes)[1].reshape(1,512,512), axis=0)
                Uminus += 1

            """There's one slight problem with this if statement: It doesn't 
            add the images for the very last polarimetric cycle in the data set. 
            I'll fix this some time. I noticed this on 25/03/2025.
            One temporary fix is to put a copy of the very first Qplus FITS 
            file at the very end of the data set, which triggers the 
            Stokes == "Qplus" part of the if statement correctly."""
            if (Qplus!=0 and Qminus!=0 and Uplus!=0 and Uminus!=0) and Stokes == "Qplus":
                #print("\nFull polarimetric cycle")
                Qplus   = 0 
                Qminus  = 0
                Uplus   = 0
                Uminus  = 0

                if n_cycles == 0:
                    Qplus_singdiff  = np.average(Qplus_singdiff_cyc, axis=0).reshape(1,512,512)
                    Qminus_singdiff = np.average(Qminus_singdiff_cyc, axis=0).reshape(1,512,512)
                    Uplus_singdiff  = np.average(Uplus_singdiff_cyc, axis=0).reshape(1,512,512)
                    Uminus_singdiff = np.average(Uminus_singdiff_cyc, axis=0).reshape(1,512,512)
                    Qplus_int  = np.average(Qplus_int_cyc, axis=0).reshape(1,512,512)
                    Qminus_int = np.average(Qminus_int_cyc, axis=0).reshape(1,512,512)
                    Uplus_int  = np.average(Uplus_int_cyc, axis=0).reshape(1,512,512)
                    Uminus_int = np.average(Uminus_int_cyc, axis=0).reshape(1,512,512)
                else:
                    Qplus_singdiff = np.append(Qplus_singdiff, np.average(Qplus_singdiff_cyc, axis=0).reshape(1,512,512), axis=0)
                    Qminus_singdiff = np.append(Qminus_singdiff, np.average(Qminus_singdiff_cyc, axis=0).reshape(1,512,512), axis=0)
                    Uplus_singdiff = np.append(Uplus_singdiff, np.average(Uplus_singdiff_cyc, axis=0).reshape(1,512,512), axis=0)
                    Uminus_singdiff = np.append(Uminus_singdiff, np.average(Uminus_singdiff_cyc, axis=0).reshape(1,512,512), axis=0)
                    Qplus_int = np.append(Qplus_int, np.average(Qplus_int_cyc, axis=0).reshape(1,512,512), axis=0)
                    Qminus_int = np.append(Qminus_int, np.average(Qminus_int_cyc, axis=0).reshape(1,512,512), axis=0)
                    Uplus_int = np.append(Uplus_int, np.average(Uplus_int_cyc, axis=0).reshape(1,512,512), axis=0)
                    Uminus_int = np.append(Uminus_int, np.average(Uminus_int_cyc, axis=0).reshape(1,512,512), axis=0)

                n_cycles += 1
                finish_time_sing_diff = time.monotonic()
                time_taken_sing_diff = finish_time_sing_diff - start_time_sing_diff
                start_time_sing_diff = time.monotonic()
                print(f"# {detector}: Single difference completed "\
                      f"for polarimetric cycle #{n_cycles:2}. Time"\
                        f" taken: {time_taken_sing_diff:.2f} s")
            else:
                pass

    Q_val = (1/2)*(Qplus_singdiff - Qminus_singdiff)
    U_val = (1/2)*(Uplus_singdiff - Uminus_singdiff)

    Int_Q = (1/2)*(Qplus_int + Qminus_int)
    Int_U = (1/2)*(Uplus_int + Uminus_int)
    Int_tot = (1/2)*(Int_Q + Int_U)
    Pol_int = np.sqrt(Q_val**2 + U_val**2)

    Q_val_ave   = np.average(Q_val[:, :, :], axis=0)
    U_val_ave   = np.average(U_val[:, :, :], axis=0)
    Int_Q_ave   = np.average(Int_Q[:, :, :], axis=0)
    Int_U_ave   = np.average(Int_U[:, :, :], axis=0)
    Int_tot_ave = np.average(Int_tot[:, :, :], axis=0)
    Pol_int_ave = np.average(Pol_int[:, :, :], axis=0)

    return Q_val_ave, U_val_ave, Int_Q_ave, Int_U_ave, Int_tot_ave, Pol_int_ave


if __name__=="__main__":

    data_dir = dir_in_str
    save_dir = saving_dir

    start_time = time.monotonic()
    print("\nScript started at: ", time.ctime())

    double_diff(data_dir, save_dir, "Callas", savesteps=save_steps)

    end_time = time.monotonic()
    print("\nTime taken: ", timedelta(seconds=end_time - start_time))
    print("\nScript finished at: \n", time.ctime())