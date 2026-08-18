"""This is the input script for the data processing pipeline. To use the pipeline, the user needs to input the
following objects:

**dir_in_str**  - The directory containing the raw FITS files from ZIMPOL to be processed

**saving_dir**  - The directory to save the processed HCI images in

**save_steps**  - Boolean. Set this to \"True\" to save FITS files for intermediate steps in the pipeline

**save_fits**   - A dictionary used to specify which FITS files for intermediate steps should be saved"""
import os

#dir_in_str = r"C:/Users/Stephen/Documents/FYP_Pipeline_Local/Data/ESO-test-data-small"
dir_in_str = os.path.join(os.getcwd(), "raw")
saving_dir = r"C:/Users/Stephen/Documents/FYP_Pipeline_Local/Data/Reduced-data/ESO-test-data-small"
save_steps = True

save_fits = {
"0 phase mode": 0,                                                      #   1
"pi phase mode": 0,                                                     #   2
"0 overscan removed": 0,                                                #   3
"pi overscan removed": 0,                                               #   4
"0 ordinary ray": 0,                                                    #   5
"0 extraordinary ray": 0,                                               #   6
"pi ordinary ray": 0,                                                   #   7
"pi extraordinary ray": 0,                                              #   8
"0 ordinary ray, star centered": 0,                                     #   9
"0 extraordinary ray, star centered": 0,                                #   10
"pi ordinary ray, star centered": 0,                                    #   11
"pi extraordinary ray, star centered": 0,                               #   12
"single difference 1024x512": 0,                                        #   13
"intensity 1024x512": 0,                                                #   14
"single difference 512x512": 0,                                         #   15
"intensity 512x512": 0,                                                 #   16
"Qplus": 0,                                                             #   17
"Qminus": 0,                                                            #   18
"Uplus": 0,                                                             #   19
"Uminus": 0,                                                            #   20
"Qplus intensity": 0,                                                   #   21
"Qminus intensity": 0,                                                  #   22
"Uplus intensity": 0,                                                   #   23
"Uminus intensity": 0,                                                  #   24
"Q double difference": 0,                                               #   25
"U double difference": 0,                                               #   26
"Q intensity": 0,                                                       #   27
"U intensity": 0,                                                       #   28
"total intensity": 0,                                                   #   29
"polarised intensity": 0,                                               #   30
"Q double difference average": 1,                                       #   31
"U double difference average": 1,                                       #   32
"Q intensity average": 0,                                               #   33
"U intensity average": 0,                                               #   34
"total intensity average": 1,                                           #   35
"polarised intensity average": 1,                                       #   36
"Q double difference corrected for instrumental polarisation": 1,       #   37
"U double difference corrected for instrumental polarisation": 1,       #   38
"polarised intensity corrected for instrumental polarisation": 1,       #   39
"Qphi (azimuthal Q)": 1,                                                #   40
"Uphi (azimuthal U)": 1,                                                #   41
"Q double difference, average of two detectors": 1,                     #   42
"U double difference, average of two detectors": 1,                     #   43
"polarised intensity, average of two detectors": 1,                     #   44
"Qphi, average of two detectors": 1,                                    #   45
"Uphi, average of two detectors": 1                                     #   46
}