from google.genai import types
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from configs import WORKING_DIR


available_functions = types.Tool(
    function_declarations=[schema_get_files_info,
                           schema_get_file_content,
                           schema_write_file,
                           schema_run_python_file
                           ],
)


def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Content:
    """
    Executes a function based on the provided FunctionCall object and returns the result
    formatted as a Content object.

    It acts as a dispatcher, looking up the function name and unpacking the arguments
    from the function_call_part.args dictionary. It also automatically injects a
    'working_directory' argument.

    Args:
        function_call_part: An object containing the name of the function to call
                            and a dictionary of its keyword arguments.
        verbose: If True, prints the full function call signature (name and args);
                 otherwise, prints only the function name.

    Returns:
        A types.Content object with the role 'tool'. The content contains a
        Part.from_function_response with the function's result or an error message
        if the function is not found.
    """
    functions = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
    }
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_to_call = functions.get(function_name)

    if function_to_call:
        function_result = function_to_call(**{**function_args, "working_directory": WORKING_DIR})
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
