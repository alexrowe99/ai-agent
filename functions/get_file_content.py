import os

MAX_FILE_SIZE = 10000

def get_file_content(working_directory, file_path):
    working_directory_files = []
    for (root, dirs, file) in os.walk(working_directory):
        for f in file:
            working_directory_files.append(os.path.join(root, f))
    full_path = os.path.join(working_directory, file_path)
    try:
        with open(full_path, 'r') as file:
            if full_path not in working_directory_files:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            content = file.read()
            if len(content) > MAX_FILE_SIZE:
                content = content[:MAX_FILE_SIZE]+f'...File "{file_path}" truncated at 10000 characters'
            return content
    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: "{file_path}"'