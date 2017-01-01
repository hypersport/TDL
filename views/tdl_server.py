from flask import render_template, session, redirect, request, flash, url_for
from . import main


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/api')
def api():
    return render_template('api.html')


@main.route('/login')
def login():
    return render_template('login.html')
