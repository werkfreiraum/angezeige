#!/usr/bin/python2
from flask import Flask

app = Flask(__name__)

@app.route("/show")
def show():
    return "P" + str(GPIO.input(14)) + str(GPIO.input(15)) + str(GPIO.input(18))

if __name__ == "__main__":
    app.run(host= '0.0.0.0')