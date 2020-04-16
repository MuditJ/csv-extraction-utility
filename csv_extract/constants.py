import os


#Path to the schema file. This is also where the directory holding the processed csvs will be stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#This is the path to the directory holding the csvs
CONFIG_DATA_PATH = os.path.join(os.environ['HOME'],'Downloads/All_CUCM-Config2')