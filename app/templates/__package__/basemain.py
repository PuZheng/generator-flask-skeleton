# -*- coding: UTF-8 -*-
import os
from flask import Flask, render_template
from flask.ext.babel import Babel

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("<%= packageName %>.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


Babel(app)
