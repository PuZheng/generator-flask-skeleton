#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
SYNOPSIS:
    initialize database, use with CAUTION!!! don't use with product environment
USAGE:
    python init_db.py
"""
from <%= packageName %>.utils import do_commit
__import__('<%= packageName %>.basemain')
from <%= packageName %>.database import db


def init_db():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    init_db()
