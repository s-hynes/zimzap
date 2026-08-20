import os
import shutil
import datetime as dt
import time
import argparse
from argparse import RawTextHelpFormatter
from astropy.io import fits
from .config_methods import make_config, read_config_file
from .steps8to10 import final_combination

def check_directories():
    """This function checks for the existence of the directory for raw FITS 
    files and the directories where the final reduced data are saved. If any of 
    these don't exist, this function creates them."""
    
    raw_data_dir = os.path.join(os.getcwd(), "raw")
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
        print(f"""\nThe raw data directory {raw_data_dir} did not exist. It was 
    created but you now need to put your raw FITS files in there.""")
        
        """I should put some kind of assert statement here to stop the whole 
        pipeline if there's no raw data."""

    for reduction_stage in ["star_pol_subtr", "no_star_pol_subtr"]:
        for detector in ["Callas", "Bartoli", "detectors_combined"]:
            path_1 = os.path.join(os.getcwd(), f"reduced_pdi/{reduction_stage}/{dt.date.today()}/{detector}/")
            if not os.path.exists(path_1):
                os.makedirs(path_1)

def file_copying_fiddle(stokes_par:str):
    raw_data_dir = os.path.join( os.getcwd(), "raw")
    one_file_copied = False
    
    for file in os.scandir(raw_data_dir):
        if not one_file_copied:
            #filename = os.fsdecode(file)
            filename = file.name
            if filename.endswith(".fits"):
                fits_file_path = os.path.join(raw_data_dir, filename)
                hdul = fits.open(fits_file_path)
                Stokes = hdul[0].header['HIERARCH ESO OCS3 ZIMPOL POL STOKES']
                hdul.close()
                if Stokes == stokes_par:
                    one_file_copied = True
                    file_copy_path = os.path.join(raw_data_dir, "Z-"+filename)
                    shutil.copyfile(fits_file_path, file_copy_path)
                    return file_copy_path

def run_pipeline():

    working_dir = os.getcwd()
    raw_data_dir = os.path.join(working_dir, "raw")
    config_file_path = os.path.join(working_dir, "config.conf")

    print("\n"+80*"#"+"\n"+80*"#")
    print("# Pipeline started at: "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print(80*"#"+"\n"+80*"#")
    start_time = time.monotonic()

    check_directories()
    file_copy_path = file_copying_fiddle("Qplus")

    perform_preprocessing, \
    sigma_filtering, \
    object_collapse_ndit, \
    object_centering_method, \
    frames_to_remove, \
    perform_pdi, \
    annulus_star, \
    annulus_background, \
    normalized_polarization_images, \
    perform_adi, \
    principal_components, \
    pca_radii, \
    center_subtract_object, \
    center_param_centering, \
    object_center_coordinates, \
    object_param_centering, \
    flux_centering_method, \
    flux_center_coordinates, \
    flux_param_centering, \
    flux_annulus_background, \
    flux_annulus_star, \
    double_difference_type, \
    single_posang_north_up, \
    combination_method_polarization, \
    combination_method_intensity \
    = read_config_file(config_file_path)

    final_combination(raw_data_dir)
    os.remove(file_copy_path)

    end_time = time.monotonic()
    print("\n"+80*"#"+"\n"+80*"#")
    print("# Pipeline finished at: "\
          f"{time.strftime('%H:%M:%S %d/%m/%y', time.gmtime())}.")
    print("# Time taken: ", dt.timedelta(seconds=end_time - start_time))
    print(80*"#"+"\n"+80*"#")

def main():

    working_dir = os.getcwd()
    # String variable for whatever name I decide to give the pipeline
    PROGRAM_NAME = "Zimzap"
    # Name of example system, if we want to have a demo dataset like IRDAP has
    # e.g. in IRDAP's case, the example system is the circumstellar disk of T Cha
    EXAMPLE_SYSTEM = "Example_system"

    # First create the parser object
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, 
            description="""Text that is printed at the top of the help message.""", 
            epilog="""Text that is printed at the bottom of the help message.""",
            formatter_class = RawTextHelpFormatter)

    # Then add arguments to the parser object using the add_argument() method
    parser.add_argument("-v", "--version",  action = "store_true", help = "show program\'s version number")

    parser.add_argument("-w", "--website", action = "store_true",
                        help = f"open {PROGRAM_NAME} online documentation in web browser")

    parser.add_argument("-p", "--print", action = "store_true",
                        help = "toggle printing of log statements in the terminal")
    
    parser.add_argument("-d", "--demo", action = "store_true",
    help = f"""run pipeline in current working directory with example data of the circumstellar disk {EXAMPLE_SYSTEM}""")
    
    parser.add_argument("-o", "--headers", action = "store_true",
                        help = """create overview of relevant headers of FITS-files in raw subdirectory""")
    
    parser.add_argument("-c", "--makeconfig", action = "store_true",
                        help = """create default configuration file in current working directory""")
    
    parser.add_argument("-r", "--run", action = "store_true", 
                        help = """run pipeline using configuration file in current working directory""")
    
    parser.add_argument("-m", "--meancombine", nargs='+', type=str, metavar='path',
                        help = "mean-combine images of two or more reductions. The \n" \
                        "absolute paths to the main directories of the reductions \n" \
                        "should be supplied as arguments and be separated by \n" \
                        "spaces.")

    args = parser.parse_args()

    if args.run:
        run_pipeline()

    if args.makeconfig:
        make_config(working_dir)

if __name__ == "__main__":
    main()