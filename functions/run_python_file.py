import os
from subprocess import run
from google.genai import types

def run_python_file(working_directory, file_path, args=[]) :

	try:

		newDir = os.path.join(working_directory, file_path)

		if not(os.path.abspath(newDir).startswith(os.path.abspath(working_directory))) :
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		if not(os.path.exists(newDir)) :
			return f'Error: File "{file_path}" not found.'
		if file_path.split(".")[-1] != "py" :
			return f'Error: "{file_path}" is not a Python file.'

		try :
			execFile = run(["python",newDir,*args], capture_output=True, timeout=30)
			return f"STDOUT: {execFile.stdout}\nSTDERR: {execFile.stderr}{'\nProcess exited with code '+str(execFile.returncode)+'\n' if execFile.returncode != 0 else ''}{'\nNo output produced' if not(execFile.stdout) else ''}"
		except Exception as e :
			return f"Error: executing Python file: {e}"

	except Exception as e :

		return f"Error: {str(e)}"

schema_run_python_file = types.FunctionDeclaration(
	name="run_python_file",
	description="Runs a python file, returning a string containing stdout, stderr, also exit code if exit code is non 0, also the launched file's output if it provides any. Constained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The file to run. Must be a python file. Must be provided.",
			),
		},
	),
)
