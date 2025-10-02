#!/usr/bin/env python
"""
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"], strict_slashes=True)
def index():
    """Return a simple JSON payload"""
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
