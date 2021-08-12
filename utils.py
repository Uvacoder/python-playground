import os
import subprocess
import uuid
from typing import Union


def execute_code(code: str) -> Union[str, bytes]:
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
            f"python3 {filename}",
            shell=True,
            stderr=subprocess.PIPE,
            env=dict(author="Amal Shaji"),
        )
    except subprocess.CalledProcessError as e:
        result = e.stderr
    # except TimeoutError:
    #     result = "Execution time exceeded 3 seconds"
    os.remove(filename)
    return result
