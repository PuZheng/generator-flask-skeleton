# -*- coding: UTF-8 -*-
import types


def do_commit(session, obj, action="add"):
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
