from appdir import app
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from appdir.config import Config

@app.route('/')
def login():
    return 'hello world'



