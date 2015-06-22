# -*- coding: UTF-8 -*-
from <%= packageName %>.database import db
from <%= packageName %>.utils import to_camel_case
from flask.ext.login import UserMixin
from <%= packageName %>.sa_types import ListType, ChoiceType

class Unicodable(object):

    @property
    def _unicode_fields(self):
        return [k for k in self.__mapper__.columns.keys() if k != 'id']

    def __unicode__(self):
        ret = self.__class__.__name__
        if self.id:
            ret += ' ' + str(self.id) + ' '
        l = []
        for field in self._unicode_fields:
            value = getattr(self, field)
            if value:
                l.append([field, value])

        return ('<' + ret + '(' + ','.join([':'.join(map(str, [k, v])) for k,
                                            v in l]) + ')' + '>')

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class JSONSerializable(object):

    def __json__(self, camel_case=True, excluded=set()):
        ret = dict((c.name, getattr(self, c.name)) for c
                   in self.__mapper__.columns if c not in excluded)
        return to_camel_case(ret) if camel_case else ret


class Foo(db.Model, JSONSerializable, Unicodable):
    __tablename__ = 'TB_FOO'

    id = db.Column(db.Integer, primary_key=True)

    def __unicode__(self):
        return 'foo'
