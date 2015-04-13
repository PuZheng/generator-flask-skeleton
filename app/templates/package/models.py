# -*- coding: UTF-8 -*-
from <%= packageName %>.database import db
from <%= packageName %>.utils import to_camel_case
from flask.ext.login import UserMixin
from <%= packageName %>.sa_types import ListType, ChoiceType

class JSONSerializable(object):

    def __json__(self, camel_case=True, excluded=set()):
        ret = dict((c.name, getattr(self, c.name)) for c
                   in self.__mapper__.columns if c not in excluded)
        return to_camel_case(ret) if camel_case else ret


class Foo(db.Model, JSONSerializable):
    __tablename__ = 'TB_FOO'

    id = db.Column(db.Integer, primary_key=True)

    def __unicode__(self):
        return 'foo'
