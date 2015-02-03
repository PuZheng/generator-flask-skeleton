# -*- coding: UTF-8 -*-

from <%= packageName %>.database import db
from flask.ext.login import UserMixin


class Foo(db.Model):
    __tablename__ = 'TB_FOO'

    id = db.Column(db.Integer, primary_key=True)

    def __unicode__(self):
        return 'foo'
