import os
from google.genai import types

def write_file(working_directory, file_path, content) :

	try:

		newDir = os.path.join(working_directory, file_path)

		if not(os.path.abspath(newDir).startswith(os.path.abspath(working_directory))) :
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

		if not(os.path.exists(os.path.dirname(newDir))) :
			os.makedirs(os.path.dirname(newDir))

		with open(newDir,"w") as f :
			contents = f.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

	except Exception as e :

		return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Writes provided content to a provided file. Constained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The file to write to, relative to the working directory. If not provided, will create a new file with the given path.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The content to write to the file. Must be provided.",
			),
		},
	),
)
