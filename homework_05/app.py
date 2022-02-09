from flask import Flask
from flask import Blueprint, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", endpoint="back")
def list_example():
    return render_template(
        "back.html",
    )


@app.route("/about/", endpoint="about")
def text():
    return render_template(
        "about.html",
    )


if __name__=='__main__':
    app.run(debug=True)