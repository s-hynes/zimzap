"""This scripts creates and reads the config file."""
import os
import shutil
from ast import literal_eval
import configparser

def make_config(main_dir_path):
    """
    Makes the config file
    """
    
    default_config_file_name = "config.conf"
    default_config_file_path = os.path.join(os.path.dirname(__file__), default_config_file_name)
    #writing_config_file_path = os.path.join(main_dir_path, os.path.basename(default_config_file_path))
    writing_config_file_path = os.path.join(main_dir_path, default_config_file_name)

    if os.path.exists(writing_config_file_path):
        overwrite = input(f"\nThe configuration file {writing_config_file_path}"
                          +" already exists. Would you like to overwite it? (y/n) ")
        if overwrite == "n":
            print("\nNo new configuration file was created.")
        elif overwrite != "y":
            print(f"\nThe provided input \"{str(overwrite)}\" is not valid.")
        
    if not os.path.exists(writing_config_file_path):
        shutil.copyfile(default_config_file_path, writing_config_file_path)
        print(f"\nCreated a default configuration file {writing_config_file_path}.")
    elif overwrite == "y":
        shutil.copyfile(default_config_file_path, writing_config_file_path)
        print("\nExisting configuration file has been overwritten with a new"\
              f" copy of the default configuration file, {writing_config_file_path}.")

def read_config_file(path_config_file):
    '''
    Read the configuration file with input parameters

    Input:
        path_config_file: string specifying path of configuration file

    Output:
        all input parameters from the configuration file

    File written by Rob van Holstein
    Function status: verified
    '''

    def config_true_false(x):
        if x in ['True', 'False']:
            return literal_eval(x)
        else:
            return x

    def config_list_tuple(x):
        if '(' in x or '[' in x:
            return literal_eval(x)
        else:
            return x

    def config_float_int(x):
        if all(character.isdigit() or character == '.' for character in x):
            return literal_eval(x)
        else:
            return x

    def config_float_int_list_tuple(x):
        if '(' in x or '[' in x:
            return literal_eval(x)
        elif all(character.isdigit() for character in x):
            return [literal_eval(x)]
        else:
            return x

    # Create a configparser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config_read = config.read(path_config_file)

    # Raise error if configuration file does not exist
    if len(config_read) == 0:
        raise IOError('\n\nThere is no valid configuration file ' + path_config_file + '.')

    # Get parameters from [Basic pre-processing options] section
    perform_preprocessing   = config_true_false(config.get('Basic pre-processing options', 'perform_preprocessing'))
    sigma_filtering         = config_true_false(config.get('Basic pre-processing options', 'sigma_filtering'))
    object_collapse_ndit    = config_true_false(config.get('Basic pre-processing options', 'object_collapse_ndit'))
    object_centering_method = config.get('Basic pre-processing options', 'object_centering_method')
    frames_to_remove        = literal_eval(config.get('Basic pre-processing options', 'frames_to_remove'))

    # Get parameters from [Basic PDI options] section
    perform_pdi                    = config_true_false(config.get('Basic PDI options', 'perform_pdi'))
    annulus_star                   = config_list_tuple(config.get('Basic PDI options', 'annulus_star'))
    annulus_background             = config_list_tuple(config.get('Basic PDI options', 'annulus_background'))
    normalized_polarization_images = config_true_false(config.get('Basic PDI options', 'normalized_polarization_images'))

    # Get parameters from [Basic ADI options] section
    perform_adi          = config_true_false(config.get('Basic ADI options', 'perform_adi'))
    principal_components = config_float_int_list_tuple(config.get('Basic ADI options', 'principal_components'))
    pca_radii            = config_list_tuple(config.get('Basic ADI options', 'pca_radii'))

    # Get parameters from [Advanced pre-processing options] section
    center_subtract_object    = config_true_false(config.get('Advanced pre-processing options', 'center_subtract_object'))
    center_param_centering    = literal_eval(config.get('Advanced pre-processing options', 'center_param_centering'))
    object_center_coordinates = config_list_tuple(config.get('Advanced pre-processing options', 'object_center_coordinates'))
    object_param_centering    = literal_eval(config.get('Advanced pre-processing options', 'object_param_centering'))
    flux_centering_method     = config.get('Advanced pre-processing options', 'flux_centering_method')
    flux_center_coordinates   = literal_eval(config.get('Advanced pre-processing options', 'flux_center_coordinates'))
    flux_param_centering      = literal_eval(config.get('Advanced pre-processing options', 'flux_param_centering'))
    flux_annulus_background   = config_list_tuple(config.get('Advanced pre-processing options', 'flux_annulus_background'))
    flux_annulus_star         = config_list_tuple(config.get('Advanced pre-processing options', 'flux_annulus_star'))

    # Get parameters from [Advanced PDI options] section
    double_difference_type          = config.get('Advanced PDI options', 'double_difference_type')
    single_posang_north_up          = config_true_false(config.get('Advanced PDI options', 'single_posang_north_up'))
    try:
        combination_method_polarization = config_float_int(config.get('Advanced PDI options', 'combination_method_polarization'))
    except:
        combination_method_polarization = 'least squares'
    try:
        combination_method_intensity    = config_float_int(config.get('Advanced PDI options', 'combination_method_intensity'))
    except:
        combination_method_intensity    = 'mean'

    return perform_preprocessing, \
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
           combination_method_intensity

if __name__ == "__main__":
    make_config(os.getcwd())
    read_config_file(os.getcwd())