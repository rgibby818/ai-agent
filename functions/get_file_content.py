from os.path import isfile, join, abspath
from functions.is_authorized import is_authorized_path
from google.genai import types
from configs import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads and returns the content of a file at the given relative file path. "
        "It won't return the entire content if the character count is above a set amount (defaults to 10,000 characters). "
        "The path must be inside the working directory. "
        "If the path is outside the working directory, does not exist, or does not point to a regular file, "
        "an error string is returned."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":
            types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the file within the working directory."
                )
            )
        },
        required=["file_path"]
    )
)


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Returns the content of a file as a string. If path is outside the working_directory
    or file_path is not a file an error string is returned.
    """
    working_absolute_path = abspath(working_directory)
    file_abolute_path = abspath(join(working_absolute_path, file_path))

    if not is_authorized_path(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not isfile(file_abolute_path):
        return f'Error: File not found or is not a regular file "{file_path}"'

    return format_content(file_abolute_path, MAX_CHARS)


def format_content(file_path: str, MAX_CHARS: int) -> str:
    try:
        with open(file_path, "r") as f:
            content = f.read(MAX_CHARS)
            has_extra = f.read(1)

            if has_extra:
                return content + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except FileNotFoundError:
        return "Error: File not found."
    except PermissionError:
        return "Error: You do not have permission to read this file"
