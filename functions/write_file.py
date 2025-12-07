from os.path import exists, abspath, join, dirname
from os import makedirs
from functions.is_authorized import is_authorized_path


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Writes (content) to a (file_path). If any errors arise an error string is returned.
    if successful a success message string is returned.
    """
    working_abs_path = abspath(working_directory)
    file_abs_path = abspath(join(working_abs_path, file_path))

    if not is_authorized_path(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not exists(file_abs_path):
        makedirs(dirname(file_path))
    try:
        with open(file_abs_path, "w") as f:
            f.write(content)
            f.write
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except BlockingIOError:
        return 'Error: Buffer is full cannot write to file'
    except FileExistsError:
        return f'Error: "{file_path}" File not Found'
    except IsADirectoryError:
        return f'Error: "{file_path}" is a directory'
    except NotADirectoryError:
        return f'Error: "{file_path}" part of the path is not a directory'
    except PermissionError:
        return f'Error: You do not have permission to write to {file_path}'
    except Exception as e:
        return f'Error: {e}'
