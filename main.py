# import signal

from deta import Deta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import api as pyplay_api
from config import settings

# def handle_func(a, b):
#     raise TimeoutError


app = FastAPI(
    title="Python Playground",
    docs_url=None,
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pyplay_api, prefix="/api")
templates = Jinja2Templates(directory="templates")

deta = Deta(settings.deta_project_key)
db = deta.Base("python_playground")
# signal.signal(signal.SIGALRM, handle_func)

default_code = """
# run this code
# playground by @pydantic deployed to deta.sh

import this
"""


@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse(
        "editor.html", {"request": request, "code": default_code}
    )


@app.get("/s/{id}")
async def load_snippet_by_id(request: Request, id: str):
    res = db.get(id)
    if res is None:
        return RedirectResponse(url="/", status_code=301)
    if res.get("description") == None:
        res["description"] = ""
    return templates.TemplateResponse(
        "editor.html",
        {"request": request, "code": res.get("code"), "desc": res.get("description")},
    )
