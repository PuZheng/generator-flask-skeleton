# -*- coding: UTF-8 -*-
import types
import random
import string
import re
import collections


def random_str(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.sample(chars, size))


def do_commit(db, obj, action="add"):
    session = db.session
    if action == "add":
        if isinstance(obj, collections.Iterable):
            session.add_all(obj)
        else:
            session.add(obj)
    elif action == "delete":
        if isinstance(obj, collections.Iterable):
            for i in obj:
                session.delete(i)
        else:
            session.delete(obj)
    session.commit()
    return obj


def to_camel_case(arg):
    if isinstance(arg, types.DictType):
        return dict((to_camel_case(k), v) for k, v in arg.items())
    assert isinstance(arg, basestring)
    return re.sub(r'_([a-z0-9])', lambda m: m.groups()[0].upper(), arg)
