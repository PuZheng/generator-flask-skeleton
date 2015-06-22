# -*- coding: UTF-8 -*-
import types
import random
import string
import re
import collections
from path import path


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


def to_underscore(arg):
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', arg)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()


def asset_for(url):
    from flask import current_app
    match = current_app.url_map.bind('').match(url)
    if match and match[0] == 'assets':
        path_ = path.joinpath(current_app.config['ASSETS_FOLDER'],
                              match[1]['filename'])
        if path_.exists():
            return path.joinpath(current_app.config['ASSETS_FOLDER'],
                                 match[1]['filename'])


def log_form_error(form):
    if form.errors:
        for k, v in form.errors.iteritems():
            print k + ':'
            for e in v:
                print '\t' + e
