# import signal

import os

from deta import Deta
from flask import Flask, jsonify, redirect, render_template, request, url_for

import utils

# def handle_func(a, b):
#     raise TimeoutError


app = Flask(__name__)
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
db = deta.Base("python_playground")
# signal.signal(signal.SIGALRM, handle_func)


@app.get("/")
def homepage():
    return render_template("editor.html")


@app.get("/s/<id>")
def read_snippet(id: int):
    snip = db.get(key=id)
    if snip is None:
        return redirect(url_for("homepage"))
    return id


@app.post("/api/run")
def execute():
    body = request.json
    code = body.get("code")
    try:
        # signal.alarm(3)
        result = utils.execute_code(code)
    except Exception:
        result = "Execution timed out(max 3 seconds)".encode()
    finally:
        # signal.alarm(0)
        pass
    return jsonify(result=str(result.decode())), 200


@app.post("/api/save")
def save_to_cloud():
    pass


if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True)
