import os
from google.genai import types


def get_files_info(working_directory, directory="."):
	working_directory_path = os.path.abspath(working_directory)
	directory_path = os.path.abspath(os.path.join(working_directory, directory))
	print(f"Result for {directory} directory:")


	if not directory_path.startswith(working_directory_path):
		print( f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
		return

	if not os.path.isdir(directory_path):
		print (f'Error: "{directory}" is not a directory')
		return

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
		print ('\n'.join(files_info))
	except Exception as e:
		return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


if __name__ == '__main__':
	get_files_info('calculator', '.')

