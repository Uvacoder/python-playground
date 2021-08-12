from fastapi import APIRouter, HTTPException, status

from .schema import CodePayload
from .utils import execute_code as execute

api = APIRouter()


@api.post("/run")
async def execute_code(payload: CodePayload):
    code = payload.code
    try:
        # signal.alarm(3)
        result = execute(code)
    except Exception:
        result = "Execution timed out(max 3 seconds)".encode()
    finally:
        # signal.alarm(0)
        pass
    return dict(result=str(result.decode()))
