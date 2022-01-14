# coding = utf8

import os

os.path.abspath(".")
from flask import Flask
import requests

app = Flask(__name__)
"""
    Flask Framework Build
"""


@app.route("/")
def hello_world():
    html = requests.get("https://idea.medeming.com/pycharm/")
    html.encoding = "utf-8"
    return html.text


@app.route("/chenguangtao")
def emmm():
    html = requests.get("https://cn.bing.com/")
    html.encoding = "utf-8"
    return html.text


@app.route("/user/<username>")
def show_user_profile(username):
    return "User's name is {}".format(username)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return "Post id is {}".format(post_id)


@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Page not found, please check your website or connect to your administrator</h1>"


if __name__ == "__main__":
    app.debug = True
    app.run()
