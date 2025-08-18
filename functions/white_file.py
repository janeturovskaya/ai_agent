import os

def write_file(working_directory, file_path, content):
	working_directory_path = os.path.abspath(working_directory)
	file_path_abs = os.path.join(working_directory_path, file_path)

	if not file_path_abs.startswith(working_directory_path):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

	if not os.path.exists(file_path_abs):
		try:
			os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
		except Exception as e:
			return f"Error: creating directory: {e}"
	if os.path.exists(file_path_abs) and os.path.isdir(file_path_abs):
		return f'Error: "{file_path}" is a directory, not a file'
	try:
		with open(file_path_abs, "w") as f:
			f.write(content)
		return (
			f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
		)
	except Exception as e:
		return f"Error: writing to file: {e}"

