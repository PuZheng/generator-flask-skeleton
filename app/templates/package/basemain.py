# -*- coding: UTF-8 -*-
import os
from flask import Flask, render_template, send_from_directory, request, abort
from flask.ext.babel import Babel
from werkzeug import secure_filename
from path import path
import sh

from <%= packageName %>.utils import random_str

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("<%= packageName %>.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/assets/<path:filename>')
def assets(filename=None):
    return send_from_directory(app.config['ASSETS_FOLDER'],
                               filename, as_attachment=True)


@app.route('/uploads', methods=['POST', 'DELETE'])
def uploads():
    if request.method == 'POST':
        file_ = request.files['file']
        if file_:
            filename = secure_filename(file_.filename)
            filename = random_str(32) + '.' + filename
            path_ = path.joinpath(app.config["ASSETS_FOLDER"],
                                  'uploads',
                                  request.args.get('type', ''))
            if not path_.exists():
                sh.mkdir('-p', path_)
            full_path = path_.joinpath(filename)
            file_.save(full_path)
            return jsonify({
                'url': url_for('.assets',
                               filename=path.joinpath('uploads',
                                                      request.args.get('type',
                                                                       ''),
                                                      filename)),
            })
        abort(403)
    else:  # DELETE
        match = app.url_map.bind('').match(request.json['url'])
        if match and match[0] == 'assets':
            path_ = path.joinpath(app.config['ASSETS_FOLDER'],
                                  match[1]['filename'])
            if path_.exists():
                sh.rm(path.joinpath(app.config['ASSETS_FOLDER'],
                                    match[1]['filename']))
            return 'ok'
        abort(404)



Babel(app)


path_ = path.joinpath(app.config['UPLOAD_FOLDER'])
if not path_.exists():
    sh.mkdir('-p', path_)


from json import JSONEncoder
import datetime


class DynamicJSONEncoder(JSONEncoder):
    """ JSON encoder for custom classes:
        Uses __json__() method if available to prepare the object.
        Especially useful for SQLAlchemy models
    """

    def default(self, o):
        # Custom JSON-encodeable objects
        if hasattr(o, '__json__'):
            return o.__json__()
        if isinstance(o, datetime.datetime):
            return o.isoformat(' ')
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, set):
            return list(o)
        # Default
        return super(DynamicJSONEncoder, self).default(o)

app.json_encoder = DynamicJSONEncoder


mail = Mail(app)


def email_exception(traceback):

    recipients = app.config.get('EXCEPTION_EMAIL_RECIPIENTS')
    if not recipients:
        return
    msg = Message(subject=_(u"failed request: %(method)s %(url)s",
                            method=request.method,
                            url=request.url),
                  html=traceback.render_summary(),
                  recipients=recipients)
    mail.send(msg)


if app.debug or app.testing:
    @app.errorhandler(Exception)
    def error(error):
        if isinstance(error, SQLAlchemyError):
            db.session.rollback()
        from werkzeug.debug.tbtools import get_current_traceback

        traceback = get_current_traceback(skip=1, show_hidden_frames=False,
                                          ignore_system_exceptions=True)
        app.logger.error("%s %s" % (request.method, request.url))
        app.logger.error(traceback.plaintext)
        email_exception(traceback)
        return render_template('error.html',
                               title=_(u"failed request: %(method)s %(url)s",
                                       method=request.method,
                                       url=request.url),
                               text=traceback.render_summary(),
                               backref=request.args.get('backref', '/'))
