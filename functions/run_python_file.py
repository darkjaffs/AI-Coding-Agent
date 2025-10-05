import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    
    absdirectory = os.path.abspath(working_directory)
    
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startwith(absdirectory):
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
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=absdirectory
        )
        
        output=[]
        
        if result.stdout:
            output.append(f'STDOUT:\n {result.stdout}')
            
        if result.stderr:
            output.append(f'STDERR:\n {result.stderr}')

        if result.returncode != 0:
            output.append(f'Process Exited With Code: {result.returncode}')
            
        return "\n".join(output) if output else "no output produced"
            
        
    except Exception as e:
        return f"Error: executing Python file: {e}"