import os
import subprocess
import uuid
from timeit import default_timer as t
from typing import Tuple


def execute_code(code: str) -> Tuple[bytes, float]:
    """
    Executes the given code in the current shell and returns the output.
    :param code: The code to execute.
    :return: The output of the executed code.
    """
    filename = f"/tmp/{str(uuid.uuid4())}.py"
    with open(filename, "w") as f:
        f.write(code)
    start = t()
    try:
        process_output = subprocess.run(
            ["python3", filename],
            shell=False,
            capture_output=True,
            env=dict(author="Amal Shaji"),
            check=True,
            timeout=3,
        )
        result = process_output.stdout
    except subprocess.CalledProcessError as e:
        result = e.stderr
    except subprocess.TimeoutExpired as e:
        result = "Maximum 3 second limit reached".encode()
    end = t()
    os.remove(filename)
    return result, end - start
