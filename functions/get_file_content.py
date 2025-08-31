import os.path
MAX_CHARS = 10000
from google.genai import types

def get_file_content(working_directory, file_path):
	working_directory_path = os.path.abspath(working_directory)
	file_path_abs = os.path.join(working_directory_path, file_path)

	if not file_path_abs.startswith(working_directory_path):
		return f'Tool: Error: Cannot read "{file_path}" as it is outside the permitted working directory'

	if not os.path.isfile(file_path_abs):
		return f'Tool: Error: File not found or is not a regular file: "{file_path}"'

	try:
		with open(file_path_abs, 'r') as file:
			contents = file.read(MAX_CHARS)
			if os.path.getsize(file_path_abs) >= MAX_CHARS:
				contents += f'Tool: [...File "{file_path}" truncated at {MAX_CHARS} characters]'
		return contents

	except Exception as e:
		return f"Tool: Error reading files: {e}"


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents of files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # "directory": types.Schema(
            #     type=types.Type.STRING,
            #     description="The directory to read files from, relative to the working directory. If not provided, read files in the working directory itself."
            # ),
	        "file_path": types.Schema(
		        type=types.Type.STRING,
		        description="Path to the file from which get the content"
	        )
        },
required=["file_path"],
    ),
)






