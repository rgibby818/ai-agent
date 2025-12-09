import subprocess
from functions.is_authorized import is_authorized_path
from os.path import isdir, abspath, join, dirname, isfile
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python script located within the working directory and returns its output. "
        "The target file must exist, must end with the .py extension, and must be located strictly "
        "inside the working directory (no absolute paths or parent-directory traversal such as '../'). "
        "The script is executed with a maximum timeout of 30 seconds. "
        "Returns a formatted string containing the script's STDOUT, STDERR, and exit code, or an "
        "error string beginning with 'Error:' if validation fails or execution raises an exception."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":
            types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the Python file to execute, from the working directory. "
                    "Must point to an existing .py file and cannot be an absolute path or contain "
                    "parent directory traversal (e.g., '../')."
                )
            ),
            "args":
            types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of command-line arguments to pass the the Python script. "
                    "Each element must be a string. Defaults to an empty list."
                ),
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    )
)


def run_python_file(working_directory: str, file_path: str, args=[]) -> str:
    """
    Executes a Python script within a specified working directory and captures its output.

    This function validates that the file exists, is a Python file (.py), and is located
    within the permitted working directory. It runs the process with a 30-second timeout.

    Args:
        working_directory (str): The absolute or relative path to the directory serving
            as the execution context (cwd).
        file_path (str): The path to the Python file to be executed, relative to the
            working_directory.
        args (list, optional): A list of command-line arguments to pass to the Python
            script. Defaults to an empty list.

    Returns:
        str: A formatted string containing:
            - STDOUT: Standard output from the script.
            - STDERR: Standard error output from the script.
            - EXIT CODE: The process exit code (or "0" on success).
            Or a string beginning with "Error:" if validation fails or an exception occurs.
    """

    working_abs_path = abspath(working_directory)
    file_abs_path = join(working_abs_path, file_path)

    if not is_authorized_path(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not isdir(dirname(file_abs_path)) or not isfile(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: File "{file_path}" is not a Python file.'
    try:
        cmd = ["python", file_abs_path]
        if args:
            cmd.extend(args)
        process = subprocess.run(cmd,
                                 capture_output=True,
                                 text=True,
                                 timeout=30,
                                 cwd=working_abs_path)

        stdout = "No output produced" if process.stdout == "" else process.stdout
        stderr = process.stderr
        exit_code = f"Process exited with code {process.exit_code}" if process.returncode != 0 else "0"
        return f"""STDOUT: {"\n\t".join(stdout.strip().split("\n"))}

STDERR: {"\n\t".join(stderr.strip().split("\n"))}

EXIT CODE: {exit_code}
        """
    except FileNotFoundError:
        return 'Error: executing Python file: File not found'
    except Exception as e:
        return f'Error: executing Python file {type(e)}: {e}'
