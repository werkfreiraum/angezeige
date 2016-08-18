#!/usr/bin/env python2
from flask import Flask
from conf.private import web_server_options
import json

port = web_server_options['port'] if 'port' in web_server_options else None
host = web_server_options['host'] if 'host' in web_server_options else None

app = Flask(__name__, static_folder='web', static_url_path='')

@app.route("/manager")
def manager():
    return app.send_static_file('manager.html')


@app.route("/")
@app.route("/reader")
def reader():
    return app.send_static_file('reader.html')

@app.route("/config.js")
def readerHtml():
    return "var config = " + json.dumps(web_server_options)

if __name__ == "__main__":
    app.run(host=host, port=port)
