# import signal

from deta import Deta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from flask import Flask, jsonify, redirect, render_template, request, url_for

from api.routes import api as pyplay_api
from config import settings

# def handle_func(a, b):
#     raise TimeoutError


flask_app = Flask(__name__)

app = FastAPI(title="Python Playground")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pyplay_api, prefix="/api")
templates = Jinja2Templates(directory="templates")

deta = Deta(settings.deta_project_key)
db = deta.Base("python_playground")
# signal.signal(signal.SIGALRM, handle_func)


@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("editor.html", {"request": request})
