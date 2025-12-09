from os.path import abspath, join, getsize, isdir
from os import listdir
from functions.is_authorized import is_authorized_path
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, contrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        required=["directory"]
    ),
)


def get_files_info(working_directory: str, directory=".") -> str:
    """
     Retrieves metadata for files with a specified directory, ensuring the path
     stays within a permitted working directory.

     Args:
         working_directory (str): The root path allowed for access.working_directory
         directory (str): The specific subdirectory to list(defaults to current directory)

     Returns:
         str: A formatted string containing file details or an error message.
    """

    working_absolute_path = abspath(working_directory)
    directory_abolute_path = abspath(join(working_absolute_path, directory))

    if not is_authorized_path(working_directory, directory):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not isdir(directory_abolute_path):
        return (f'Error: "{directory}" is not a directory')
    if not isdir(working_directory):
        raise ValueError("working_directory is not a valid directory")

    file_infos = ""

    for item in listdir(directory_abolute_path):
        string = agent_string_format(join(directory_abolute_path, item))
        file_infos += string
    return file_infos.rstrip("\n")


def agent_string_format(file_path: str) -> str:
    # Helper function to format file metadata (name, size, type).

    try:
        filename = file_path.split("/")[-1]
        file_size = getsize(file_path)
        is_dir = isdir(file_path)
        return (f' - {filename}: file_size={file_size} bytes, is_dir={is_dir}\n')
    except FileNotFoundError as e:
        return f'Error: File not found ({e})'
    except Exception as e:
        return f'Error: {e}'


if __name__ == "__main__":
    print(schema_get_files_info)
