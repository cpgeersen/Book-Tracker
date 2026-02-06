from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def create_app():
    # Creates the most basic Flask instance to test
    return app