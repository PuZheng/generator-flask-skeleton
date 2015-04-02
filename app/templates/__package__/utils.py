# -*- coding: UTF-8 -*-
import types


def do_commit(db, obj, action="add"):
    session = db.session
    if action == "add":
        if isinstance(obj, types.ListType) or \
           isinstance(obj, types.TupleType):
            session.add_all(obj)
        else:
            session.add(obj)
    elif action == "delete":
        session.delete(obj)
    session.commit()
    return obj
