from flask import Flask
from back.config import app


@app.route("/")
def test():
    return "App Working"


if __name__ == '__main__':
    app.run(port=8080)