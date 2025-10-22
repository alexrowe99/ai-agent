import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python script at the given file path with the given args, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path from which the python script is run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to run the script with.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_directory_files = []
    for (root, dirs, file) in os.walk(working_directory):
        for f in file:
            working_directory_files.append(os.path.join(root, f))
    full_path = os.path.join(working_directory, file_path)
    try:
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if full_path not in working_directory_files:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        completed_process = subprocess.run(['uv','run',file_path,*args], capture_output=True, timeout=30000,cwd=working_directory)
    except Exception as e:
        return f'Error: executing Python file: "{e}"'
    if not completed_process.stdout and not completed_process.stderr:
        return_value = f'No output produced'
    else:
        return_value = f'STDOUT: {str(completed_process.stdout)} STDERR:{str(completed_process.stderr)}'
    if completed_process.returncode > 0:
        return_value += f' Process exited with exit code {completed_process.returncode}'
    return return_value