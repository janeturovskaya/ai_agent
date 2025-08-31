from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

def call_function(function_call_part, verbose=False):
    # if not hasattr(function_call_part, "function_call") or function_call_part.function_call is None:
    #     raise ValueError("Tool: call_function expected a Part with function_call")

    args = dict(function_call_part.args or {}) #{'file_path': 'render.py', 'directory': 'pkg'}
    args['working_directory'] = "./calculator"

    if verbose:
        args_str = ", ".join(f"{k}={v!r}" for k, v in args.items())
        print(f"Tool: Calling function: {function_call_part.name}({args_str})")
    else:
        print(f"Tool: - Calling function: {function_call_part.name}")

    match function_call_part.name:
        case 'get_file_content':
            res = get_file_content(**args)
        case 'get_files_info':
            res = get_files_info(**args)
        case 'write_file':
            res = write_file(**args)
        case 'run_python_file':
            res = run_python_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": res},
            )
        ],
    )
