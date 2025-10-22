import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
import sys

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name = 'gemini-2.0-flash-001'

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
		schema_get_file_content,
		schema_run_python_file,
		schema_write_file
    ]
)

def verbose():
	return len(sys.argv) == 3 and sys.argv[2] == '--verbose'

def main():
	if len(sys.argv) != 2 and len(sys.argv) != 3:
		print('Usage: uv run main.py (prompt) --verbose?')
		sys.exit(1)

	client = genai.Client(api_key=api_key)
	user_prompt = sys.argv[1]
	messages = [
		types.Content(role='user', parts=[types.Part(text=user_prompt)])
	]
	system_instruction_content = types.Content(role='user', parts=[types.Part(text=system_prompt)])

	response = client.models.generate_content(
		model=model_name,
		contents=messages,
		config=types.GenerateContentConfig(
			tools=[available_functions], system_instruction=system_instruction_content
		)
	)
	if response.function_calls and len(response.function_calls) > 0:
		for function_call in response.function_calls:
			response_content = call_function(function_call, verbose())
			if not response_content.parts[0].function_response.response:
				raise NameError
			if verbose():
				print(f"-> {response_content.parts[0].function_response.response}")
	print(response.text)
	if verbose():
		print(f'User prompt: {user_prompt}')
		print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
		print(f'Response tokens: {response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
	main()
