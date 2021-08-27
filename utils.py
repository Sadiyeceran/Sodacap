import configparser
import glob
import os


#read thr config file 
def read_config_file(config_file_name):
    
    config = configparser.ConfigParser()
    config.read(config_file_name)

    version = config.get('VersionInfo', 'version')
    print("version: [", version, "]")
    
    debug = config.get('Configuration', 'debug')
    print("debug: [", debug, "]")
    
    dataset_path = config.get('Configuration', 'dataset_path')
    
    output_path = config.get('Configuration', 'output_path')

    return version, debug, dataset_path, output_path


  
#get all data names in data folder 
def get_all_file_names_in_folder(folder_name, image_file_type):
    
    os.chdir(folder_name)
    file_names = []
    for file in glob.glob("*" + image_file_type):
        file_names.append(file)
    return file_names



