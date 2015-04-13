#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
    python make_test_data.py
OPTIONS:
"""
from werkzeug.security import generate_password_hash
from <%= packageName %>.database import db
from <%= packageName %>.models import Foo
from <%= packageName %>.utils import do_commit

if __name__ == "__main__":

    from <%= packageName %>.scripts.init_db import init_db
    init_db()
