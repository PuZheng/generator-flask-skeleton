# -*- coding: UTF-8 -*-

from <%= packageName %>.basemain import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
