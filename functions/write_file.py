from os.path import exists, abspath, join, dirname
from os import makedirs
from functions.is_authorized import is_authorized_path
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes the provided text content to a file located at the given relative file path "
        "inside the working directory. "
        "The file path must stay within the working directory and may not use absolute paths or "
        "parent directory traversal (e.g., '../'). "
        "If the file or its parent directories do not exist, they will be created automatically. "
        "Returns a success message on a successful write, or an error string if writing fails, "
        "including errors for invalid paths, permission issues, or attempts to write to directories."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":
            types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path (from the working directory) of the file to write to. "
                    "Must not be an absolute path and must not escape the working directory. "
                    "Intermediate directories will be created automatically if missing."
                )
            ),
            "content":
            types.Schema(
                type=types.Type.STRING,
                description=(
                    "The full text content to write into the file. "
                    "The file will be overwirtten with this content."
                )
            )
        },
        required=["file_path", "content"]
    )
)


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
        try:
            makedirs(dirname(file_abs_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
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


if __name__ == "__main__":
    print(schema_write_file)
