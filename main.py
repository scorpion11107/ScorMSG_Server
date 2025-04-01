from flask import Flask, render_template, request, jsonify

# sets log level
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import core

app = Flask(__name__)

# web home
@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    return jsonify(core.login(username, password))

@app.route("/logout", methods = ["POST"])
def logout():
    data = request.get_json()
    username = data.get("username")

    return jsonify(core.logout(username))

@app.route("/register", methods = ["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    return jsonify(core.register(username, password))

@app.route("/me", methods = ["GET"])
def get_user_info():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer:"):
        return jsonify({"status": "error", "message": "Missing token"})

    token = auth.split(":")[1]
    username = core.get_username_from_token(token)
    if not username:
        return jsonify({"status": "error", "message": "Invalid or expired session"})

    data = core.get_user_info_from_username(username)

    return jsonify({"status": "success", "data": data})

# run server
if __name__ == "__main__":

    app.run(host = "0.0.0.0", port = 4443, ssl_context = ("cert.pem", "key.pem"))