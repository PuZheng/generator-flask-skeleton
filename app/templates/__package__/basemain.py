# -*- coding: UTF-8 -*-
import os
from flask import Flask, render_template, send_from_directory
from flask.ext.babel import Babel
from path import path
import sh

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("<%= packageName %>.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/uploads/<path:filename>')
def uploads(filename=None):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


Babel(app)


path_ = path.joinpath(app.config['UPLOAD_FOLDER'])
if not path_.exists():
    sh.mkdir('-p', path_)
