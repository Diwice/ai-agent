import os
import sys
from usersettings import *
from dotenv import load_dotenv
from google.genai import Client,types
from functions.write_file import write_file,schema_write_file
from functions.get_files_info import get_files_info,schema_get_files_info
from functions.run_python_file import run_python_file,schema_run_python_file
from functions.get_file_content import get_file_content,schema_get_file_content

def call_function(function_call_part, verbose=False) :

	argsCopy = function_call_part.args.copy() if function_call_part.args else {}
	argsCopy.update({'working_directory':workingDirectory})

	verbose and print(f"Calling function: {function_call_part.name}({argsCopy})")
	not(verbose) and print(f" - Calling function: {function_call_part.name}")

	funcsDict = {"write_file":write_file,"get_files_info":get_files_info,"run_python_file":run_python_file,"get_file_content":get_file_content}
	calledFunc = funcsDict.get(function_call_part.name)

	if not(calledFunc) :
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_call_part.name,
					response={"error": f"Unknown function: {function_call_part.name}"},
				)
			],
		)

	resp = calledFunc(**argsCopy)

	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=function_call_part.name,
				response={"result": resp},
			)
		],
	)

def main() :

	len(sys.argv) < 2 and (print('Usage : ... run main.py "<prompt_to_ask>" <optional_flags> (--verbose / --iterationLimit=<num>)') or sys.exit(1))

	shouldVerbose = "--verbose" in sys.argv
	shouldVerbose and print(f"User prompt: {sys.argv[1]}")

	system_prompt = systemPrompt

	available_functions = types.Tool(
		function_declarations=[
			schema_get_files_info,
			schema_get_file_content,
			schema_run_python_file,
			schema_write_file,
		]
	)

	config = types.GenerateContentConfig(
		tools=[available_functions], system_instruction=system_prompt
	)

	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = Client(api_key=api_key)

	messages = [
		types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
	]

	def generate_content(iteration_limit) :
		nonlocal messages

		try:

			while iteration_limit :

				response = client.models.generate_content(
					model='gemini-2.0-flash-001',
					contents=messages,
					config=config,
				)

				if response.candidates :
					for c in response.candidates :
						messages.append(c.content)

				if response.function_calls :
					for fc in response.function_calls :

						function_call_result = call_function(fc, shouldVerbose)

						try :
							function_call_result.parts[0] and shouldVerbose and print(f"-> {function_call_result.parts[0].function_response.response}")
							function_call_result.parts[0] and messages.append(types.Content(role="user",parts=function_call_result.parts))
						except Exception as e :
							raise OSError(f"You're on your own, good luck : {e}")

				shouldVerbose and print(f"Prompt tokens: {response.usage_metadata.prompt_tokens_details[0].token_count}\nResponse tokens: {response.usage_metadata.candidates_tokens_details[0].token_count}")

				iteration_limit -= 1

				if not(response.function_calls) and response.text :
					break

			print(f"Final response :\n{response.text}" if response.text else "Exceeded iteration limit")

		except Exception as e :
			shouldVerbose and print(f"Exception/Error occured : {e}")

	return generate_content

if __name__ == "__main__" :
	main()(15 if not(any(i for i in sys.argv if "--iterationLimit" in i)) else int(next((i for i in sys.argv if "--iterationLimit" in i)).split("=")[-1]))
