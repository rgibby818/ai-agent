import subprocess
from functions.is_authorized import is_authorized_path
from os.path import isdir, abspath, join, dirname, isfile


def run_python_file(working_directory: str, file_path: str, args=[]) -> str:
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
