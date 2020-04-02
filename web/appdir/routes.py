from appdir import app
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from appdir.config import Config

@app.route("/")
def index():
    return "<h1>Hello World</h1>"



