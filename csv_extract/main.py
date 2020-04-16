import os,json,csv
import csv_extract.exceptions as exceptions

#Path to the schema file. This is also where the directory holding the processed csvs will be stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#This is the path to the directory holding the csvs
CSV_DIR = os.path.join(os.environ['HOME'],'Downloads/All_CUCM-Config2')


def handle_exceptions(schema_file,csv_dir,base_dir = BASE_DIR):

	#Ensuring that the directory path arguments are correct/valid

	if os.path.exists(base_dir):

		if os.path.exists(os.path.join(base_dir,schema_file)):
			#Path to schema file is valid and present.
			pass
		else:
			#Raise SchemaNotFoundError
			raise exceptions.SchemaNotFoundError("""The specified schema file was not found. Please re-check the name provided. """)

	else:
		#The path specified as the base_dir does not exist
		raise exceptions.BaseDirectoryError("""Specified base directory path does not exist. Please check the input provided.
				This should be the directory holding your JSON schema file""")
		
	#Same validation checks for csv_dir
	if os.path.exists(csv_dir):
		pass
	else:
		raise exceptions.CSVDirectoryError(""" Specified directory for the CSVs which are to be analyzed does not exist. Please check the input provided """)

	#Creating a sub-directory in the base directory to hold new csvs with extracted field data
		
	try:
		os.mkdir(os.path.join(base_dir,'extracted-data'))
	except FileExistsError:
		pass
	finally:
		#print('Finally')
		os.chdir(os.path.join(base_dir,'extracted-data'))
		print(os.getcwd())

def extract_fields(schema_file, csv_dir, base_dir = BASE_DIR):
	""" Business logic for the package

	Method signature:
	extract_fields(schema_file, csv_dir,base_dir = BASE_DIR)

	It takes the following arguments:

	schema_file:  Name of the json schema file to be analyzed for fields to extract. To try things out, pass the schema.json file present already
	
	csv_dir: This is the path to the directory holding the csvs from which data is to be extracted. 
	
	base_dir: Path to the schema file. This will be joined with the schema_file argument to open and read the JSON schema file
	This is also where the extracted-data subdirectory holding the processed csvs will be stored

	"""

	#Do exception handling:
	handle_exceptions(schema_file,csv_dir,base_dir)

	#Core logic
	schema_path = os.path.join(base_dir,schema_file)
	with open(schema_path,'r') as json_file:
		try:
			json_data = json.load(json_file)
		except json.decoder.JSONDecodeError as e:
			print('The JSON Schema is incorrect. No output csvs will be created')
			#print(f' In the JSON file:' + str(e))
			return
		else:
			clusters = json_data['clusters']
			files  = [x['file'] for x in json_data['data']]
			fields = [x['fields'] for x in json_data['data']]


			for file,required_fields in zip(files,fields):
				for cluster in clusters:
					file_name = cluster + file
					print(file_name)
					with open(os.path.join(csv_dir,file_name),'r') as csv_file:
						reader = csv.reader(csv_file)
						field_headers = next(reader)
						all_fields = {val:ind for ind,val in enumerate(field_headers)}
						if any (field not in field_headers for field in required_fields):
							raise exceptions.SchemaMismatchError('The specified fields for the file {} in the JSON schema file do not match up with the actual fields present in it.'.format(file))
							return
						else:
							target_indices = [all_fields[field] for field in required_fields]
							with open(file,'a') as target_file:
								writer = csv.writer(target_file)
								writer.writerow(required_fields)
								for row in reader:
									writer.writerow([row[index] for index in target_indices])
