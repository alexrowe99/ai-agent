import os

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    working_directory_files = os.listdir(working_directory)
    if directory not in working_directory_files and directory != '.':
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(path)
    return_string = ''
    for file in files:
        filesize = os.path.getsize(os.path.join(path,file))
        isdir = os.path.isdir(os.path.join(path,file))
        return_string += f'- {file}: file_size={filesize} bytes, is_dir={isdir}\n'
    return return_string