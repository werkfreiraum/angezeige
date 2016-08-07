#!/usr/bin/env python2
from flask import Flask

app = Flask(__name__, static_folder='web', static_url_path='')


@app.route("/manager")
def manager():
    return app.send_static_file('manager.html')


@app.route("/")
@app.route("/reader")
def reader():
    return app.send_static_file('reader.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
