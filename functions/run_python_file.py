import os
import subprocess
from google.genai import types  # type: ignore


def run_python_file(working_directory, file_path, args=[]):

    absdirectory = os.path.abspath(working_directory)

    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(absdirectory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands, capture_output=True, text=True, timeout=30, cwd=absdirectory
        )
        output = []

        if result.stdout:
            output.append(f"STDOUT:\n {result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n {result.stderr}")
        if result.returncode != 0:
            output.append(f"Process Exited With Code: {result.returncode}")
        return "\n".join(output) if output else "no output produced"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
