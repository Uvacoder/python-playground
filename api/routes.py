from config import settings
from deta import Deta
from fastapi import APIRouter

from .schema import CodePayload
from .utils import execute_code as execute

api = APIRouter()

deta = Deta(settings.deta_project_key)
db = deta.Base("python_playground")


@api.post("/run")
async def execute_code(payload: CodePayload):
    code = payload.code
    try:
        # signal.alarm(3)
        result, time = execute(code)
    except Exception:
        result = "Execution timed out(max 3 seconds)".encode()
    finally:
        # signal.alarm(0)
        pass
    return dict(result=str(result.decode()), time=time)


@api.post("/save")
async def save_code_snippet(payload: CodePayload):
    code = payload.code
    existing = db.fetch(query={"code": code}).items
    if len(existing) != 0:
        return existing[0]
    return db.put(data={"code": code, "description": payload.description})
