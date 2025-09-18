import os
from google.genai import types

def get_files_info(working_directory, directory=".") :

	try: #5

		newDir = os.path.join(working_directory, directory)

		if not(os.path.abspath(newDir).startswith(os.path.abspath(working_directory))) : #2
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not(os.path.isdir(newDir)) : #3
			return f'Error: "{directory}" is not a directory'

		resList = []
		for i in os.listdir(newDir) : #4
			resList.append(f" - {i}: file_size={os.path.getsize(os.path.join(newDir,i))}, is_dir={os.path.isdir(os.path.join(newDir,i))}")

		return "\n".join(resList)

	except Exception as e :

		return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
	name="get_files_info",
	description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"directory": types.Schema(
				type=types.Type.STRING,
				description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
			),
		},
	),
)
