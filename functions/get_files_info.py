import os


def get_files_info(working_directory, directory="."):
	working_directory_path = os.path.abspath(working_directory)
	directory_path = os.path.abspath(os.path.join(working_directory, directory))
	print(f"Result for {directory} directory:")


	if not directory_path.startswith(working_directory_path):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	if not os.path.isdir(directory_path):
		return f'Error: "{directory}" is not a directory'

	try:
		files_info = []
		for filename in os.listdir(directory_path):
			filepath = os.path.join(directory_path, filename)
			file_size = 0
			is_dir = os.path.isdir(filepath)
			file_size = os.path.getsize(filepath)
			files_info.append(
				f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
			)
		return '\n'.join(files_info)
	except Exception as e:
		return f"Error listing files: {e}"


if __name__ == '__main__':
	get_files_info('calculator', '.')

