import json
import signal

from flask import Flask, jsonify, render_template, request

import utils


def handle_timeout(signum, frame):
    raise TimeoutError


app = Flask(__name__)
# signal.signal(signal.SIGALRM, handle_timeout)


@app.get("/")
def homepage():
    return render_template("editor.html")


@app.post("/api/run")
def execute():
    # # signal.alarm(3)
    body = request.json
    code = body.get("code")
    # # try:
    # #     result = eval(code)
    # #     return jsonify(result=result), 200
    # # except TimeoutError:
    # #     return jsonify(error="Execution timed out"), 500
    # # finally:
    # #     signal.alarm(0)

    result = utils.execute_code(code)

    # signal.alarm(0)
    return jsonify(result=str(result.decode())), 200


if __name__ == "__main__":
    app.run(debug=True)
