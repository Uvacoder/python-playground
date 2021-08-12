# import signal

from flask import Flask, jsonify, render_template, request

import utils

# def handle_func(a, b):
#     raise TimeoutError


app = Flask(__name__)
# signal.signal(signal.SIGALRM, handle_func)


@app.get("/")
def homepage():
    return render_template("editor.html")


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


if __name__ == "__main__":
    app.run(debug=True)
