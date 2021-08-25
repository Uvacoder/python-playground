from config import settings
from deta import Deta
from fastapi import APIRouter, Query

from .schema import CodePayload
from .utils import execute_code as execute

api = APIRouter()

deta = Deta(settings.deta_project_key)
db = deta.Base("python_playground")


# @api.post("/run")
# async def execute_code(payload: CodePayload):
#     code = payload.code
#     try:
#         result, time = execute(code)
#     except Exception as e:
#         result = "Undocumented error"
#         time = 0
#     return dict(result=result, time=time)


@api.post("/save")
async def save_code_snippet(payload: CodePayload):
    code = payload.code
    existing = db.fetch(query={"code": code}).items
    if len(existing) != 0:
        existing_code: dict = existing[0]
        without_id = existing_code.copy()
        without_id.pop("key")
        if without_id == payload.dict(exclude={"id"}):
            return existing_code
    return db.put(
        data={"code": code, "description": payload.description}, key=payload.id
    )


@api.get("/code/{id}")
async def get_coded_by_id(id: str):
    return db.get(key=id)


@api.get("/snippets")
async def get_all_snippets(last: str = Query(None)):
    data = db.fetch(limit=10, last=last)
    return {
        "items": data.items,
        "last": data.last,
    }
