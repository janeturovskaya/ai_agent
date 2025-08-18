import os.path
MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
	working_directory_path = os.path.abspath(working_directory)
	file_path_abs = os.path.join(working_directory_path, file_path)

	if not file_path_abs.startswith(working_directory_path):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

	if not os.path.isfile(file_path_abs):
		return f'Error: File not found or is not a regular file: "{file_path}"'

	try:
		with open(file_path_abs, 'r') as file:
			contents = file.read(MAX_CHARS)
			if os.path.getsize(file_path_abs) >= MAX_CHARS:
				contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
		return contents

	except Exception as e:
		return f"Error reading files: {e}"









