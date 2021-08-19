from deta import Deta
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import api as pyplay_api
from config import settings

app = FastAPI(
    title="Python Playground",
    docs_url=None,
    redoc_url=None,
)
app.mount("/_app", StaticFiles(directory="./web/build/_app"), name="static")
app.include_router(pyplay_api, prefix="/api")
templates = Jinja2Templates(directory="./web/build")

deta = Deta(settings.deta_project_key)
db = deta.Base("python_playground")

default_code = """
# run this code
# playground by @pydantic deployed to deta.sh

import this
"""


@app.get("/")
@app.get("/{path:path}")
async def serve_index_page(path: str, request: Request):
    return templates.TemplateResponse(
        "base.html",
        {"request": request},
    )


# @app.get("/")
# async def homepage(request: Request):
#     return templates.TemplateResponse(
#         "editor.html", {"request": request, "code": default_code}
#     )


# @app.get("/s/{id}")
# async def load_snippet_by_id(request: Request, id: str):
#     res = db.get(id)
#     if res is None:
#         return RedirectResponse(url="/", status_code=301)
#     if res.get("description") == None:
#         res["description"] = ""
#     return templates.TemplateResponse(
#         "editor.html",
#         {"request": request, "code": res.get("code"), "desc": res.get("description")},
#     )


@app.on_event("startup")
async def startup():
    import subprocess

    subprocess.run("npm run --prefix web build", shell=True)
