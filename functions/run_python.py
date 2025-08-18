import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
	working_directory_path = os.path.abspath(working_directory)
	file_path_abs = os.path.abspath(os.path.join(working_directory_path, file_path))

	try:
		if os.path.commonpath([file_path_abs, working_directory_path]) != working_directory_path:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	except Exception:
		# In case commonpath raises on different drives, treat as outside
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


	if not os.path.exists(file_path_abs):
			return f'Error: File "{file_path}" not found.'


	if not file_path_abs.endswith('.py'):
		return f'Error: "{file_path}" is not a Python file.'

	extra_args = list(args) if args is not None else []
	try:
		completed_process = subprocess.run(
			[sys.executable, file_path_abs, *extra_args],
			cwd=working_directory_path,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			timeout=30)
		if not completed_process.stdout:
			stdout_string = "No output produced."
		else:
			stdout_string = f"STDOUT:{completed_process.stdout}"

		stderr_string = f"STDERR:{completed_process.stderr}"

		return f"{stderr_string}\n{stdout_string}"



	except Exception as e:
		return f"Error: executing Python file: {e}"



