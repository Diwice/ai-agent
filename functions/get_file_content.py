import os
from google.genai import types
from functions.config import *

def get_file_content(working_directory, file_path) :

	try:

		newDir = os.path.join(working_directory, file_path)

		if not(os.path.abspath(newDir).startswith(os.path.abspath(working_directory))) :
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		if not(os.path.isfile(newDir)) :
			return f'Error: File not found or is not a regular file: "{file_path}"'

		with open(newDir,"r") as f :
			contents = f.read(READ_CHAR_LIMIT)
		return contents+f"""\n{'File "'+str(file_path)+'" truncated at '+str(READ_CHAR_LIMIT)+' characters' if len(contents) == READ_CHAR_LIMIT else ''}"""

	except Exception as e :

		return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="Reads from a file making a string, truncates the output to 10000 characters if the file exceeds them. Constained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The file to read from, relative to the working directory. Must be provided.",
			),
		},
	),
)
