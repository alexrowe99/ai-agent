import os

def write_file(working_directory, file_path, content):
    working_directory_files = []
    for (root, dirs, file) in os.walk(working_directory):
        for f in file:
            working_directory_files.append(os.path.join(root, f))
    full_path = os.path.join(working_directory, file_path)
    try:
        with open(full_path, 'w') as file:
            if full_path not in working_directory_files:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            file.write(content)
    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'