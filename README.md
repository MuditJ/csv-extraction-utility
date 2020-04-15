This is a simple utility tool to extract specific fields data from the CUCM
config data using a user provided JSON schema file. A couple of sample 
JSON schema files are provided to specify the structure that is required.

Steps:

Ideally, create a virtual environment before starting:
python3 -m venv env
source env/bin/activate

From the base directory, the utility tool can be run from the commandline after import:
from src import extract_fields

View the documentation for the method using help:
help(extract_fields)


By default, the program looks for the JSON schema file in the base directory where the two sample JSON files are stored. 
This is also where the directory holding the csvs with the extracted fields 
will be stored under the directory name "extracted-data"

