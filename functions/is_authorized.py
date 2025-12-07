from os.path import abspath, join


def is_authorized_path(approved_directory: str, current_directory: str) -> bool:
    """
        Checks if the current directory is nested within (or equal to) the approved directory.
    """
    approved_directory_absolute_path = abspath(approved_directory)
    current_directory_absolute_path = abspath(join(approved_directory_absolute_path, current_directory))

    if len(approved_directory_absolute_path) > len(current_directory_absolute_path):
        return False
    return True
