# Custom exceptions defined here

class SchemaNotFoundError(Exception):
	pass

class BaseDirectoryError(Exception):
	pass

class CSVDirectoryError(Exception):
	pass

class SchemaMismatchError(Exception):
	""" Raised when the JSON schema doesnt match up with the actual CSV files and their fields which are to be analyzed """
	pass
class SchemaValidationError(Exception):
	""" Raised when the JSON passed is not validated. This is simply a wrapper over json.DecodeError """
	
	def __init__(self,msg,original_exception):
		super().__init__(msg + '{}'.format(str(original_exception)))
		self.original_exception = original_exception
	
