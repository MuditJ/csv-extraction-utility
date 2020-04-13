import os,json,csv
from exceptions import SchemaNotFoundError 


#Path to the schema file. This is also where the directory holding the processed csvs will be stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#This is the path to the directory holding the csvs
CSV_DIR = os.path.join(os.environ['HOME'],'Downloads/All_CUCM-Config2')

#Name of the json schema file to be analyzed for fields to be extracted. 
SCHEMA_FILE = 'schema.json'


def extract_fields():
	pass

def main():

	try:
		os.mkdir(os.path.join(BASE_DIR,'extracted-data'))
	except FileExistsError:
		pass
	finally:
		print('Finally')
		os.chdir(os.path.join(BASE_DIR,'extracted-data'))
		print(os.getcwd())

	print(len(os.listdir(CSV_DIR)))
	schema_path = os.path.join(BASE_DIR,SCHEMA_FILE)
	print(schema_path)

	with open(schema_path,'r') as json_file:
		json_data = json.load(json_file)
	clusters = json_data['clusters']
	files  = [x['file'] for x in json_data['data']]
	fields = [x['fields'] for x in json_data['data']]


	for file,required_fields in zip(files,fields):
		for cluster in clusters:
			file_name = cluster + file
			print(file_name)
			with open(os.path.join(CSV_DIR,file_name),'r') as csv_file:
				reader = csv.reader(csv_file)
				field_headers = next(reader)
				all_fields = {val:ind for ind,val in enumerate(field_headers)}
				target_indices = [all_fields[field] for field in required_fields]
				with open(file,'a') as target_file:
					writer = csv.writer(target_file)
					writer.writerow(required_fields)
					for row in reader:
						writer.writerow([row[index] for index in target_indices])


if __name__ == "__main__":
	main()