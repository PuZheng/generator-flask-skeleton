#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Usage:
    runserver.py [options]
OPTIONS:
    -h
        show this help
    -p [port]
        use this port
    -s [ip]
        bind this ip
"""
import sys
import getopt

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:s:")
    except getopt.GetoptError as err:
        print str(err)
        print __doc__
        sys.exit(2)

    port = None
    ip = '0.0.0.0'
    for o, a in opts:
        if o == '-h':
            print __doc__
            sys.exit(1)
        elif o == '-p':
            port = int(a)
        elif o == '-s':
            ip = a

    from <%= packageName %>.basemain import app
    app.run(debug=True, host=ip, port=port)
