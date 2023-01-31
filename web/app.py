"""
Austin Montgomery's Flask API.
"""

from flask import Flask, abort, send_from_directory
import os
import configparser

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
debug = config["SERVER"]["DEBUG"]
port = config["SERVER"]["PORT"]

app = Flask(__name__)

@app.route("/<path:request>")
@app.route("/<string:name>/<string:msg>")
def hello(request):
    if ".." in request or "~" in request:
        abort(403)
    return send_from_directory('pages/', request), 200

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def forbidden(e):
    return send_from_directory('pages/', '404.html'), 404

if __name__ == "__main__":
    app.run(debug=debug, host='0.0.0.0', port=port)
    #app.run(debug=True, host='0.0.0.0', port=5156)

