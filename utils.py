import os
import subprocess
import uuid


def execute_code(code: str) -> str:
    """
    Executes the given code in the current shell and returns the output.
    :param code: The code to execute.
    :return: The output of the executed code.
    """
    filename = f"/tmp/{str(uuid.uuid4())}.py"
    with open(filename, "w") as f:
        f.write(code)
    try:
        result = subprocess.check_output(
            f"python {filename}", shell=True, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        result = e.stderr
    # except TimeoutError:
    #     result = "Execution time exceeded 3 seconds"
    os.remove(filename)
    return result
