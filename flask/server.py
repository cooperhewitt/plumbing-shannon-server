#!/usr/bin/env python

import os
import os.path

import flask
from flask_cors import cross_origin 
import werkzeug
import werkzeug.security

import shannon
import Image

import logging
import tempfile
import base64

app = flask.Flask(__name__)

def get_path():

    path = flask.request.args.get('path')
    logging.debug("request path is %s" % path)

    root = app.config.get('SHANNON_SERVER_IMAGE_ROOT', None)
    logging.debug("image root is %s" % root)

    if not root:
        logging.error("image root is not defined")
        flask.abort(400)

    if root:

        safe = werkzeug.security.safe_join(root, path)

        if not safe:
            logging.error("'%s' + '%s' considered harmful" % (root, path))
            flask.abort(400)

        path = safe

    logging.debug("final request path is %s" % path)
    
    if not os.path.exists(path):
        logging.error("%s does not exist" % path)
        flask.abort(404)

    return path

def get_upload():

    file = flask.request.files['file']

    if file and allowed_file(file.filename):

        tmpdir = tempfile.gettempdir()

        rand = base64.urlsafe_b64encode(os.urandom(12))
        secure = werkzeug.secure_filename(file.filename)

        fname = "shannon-%s-%s" % (rand, secure)

        safe = werkzeug.security.safe_join(tmpdir, fname)
        logging.debug("save upload to %s" % safe)

        file.save(safe)
        return safe

    flask.abort(400)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/ping', methods=['GET'])
@cross_origin(methods=['GET'])
def ping():
    rsp = {'stat': 'ok'}
    return flask.jsonify(**rsp)

@app.route('/entropy', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def entropy():

    return  _shannon('entropy')

@app.route('/focalpoint', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def focalpoint():

    return _shannon('focalpoint')

def _shannon(action):

    if flask.request.method=='POST':
        path = get_upload()
    else:
        path = get_path()

    logging.debug("%s %s %s" % (flask.request.method, action, path))

    ok = True

    try:

        im = Image.open(path)

        if action == 'focalpoint':
            rsp = shannon.focalpoint(im)
        elif action == 'entropy':
            e = shannon.entropy(im)
            rsp = { 'entropy': e }
        else:
            raise Exception, "Invalid action"

    except Exception, e:
        logging.error("failed to process %s, because %s" % (path, e))
        ok = False

    if flask.request.method=='POST':
        os.unlink(path)

    if not ok:
        flask.abort(500)

    return flask.jsonify(**rsp)
    
if __name__ == '__main__':

    import sys
    import optparse
    import ConfigParser

    parser = optparse.OptionParser()

    parser.add_option("-c", "--config", dest="config", help="", action="store", default=None)
    parser.add_option("-d", "--debug", dest="debug", help="enable chatty logging; default is false", action="store_true", default=False)

    opts, args = parser.parse_args()

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cfg = ConfigParser.ConfigParser()
    cfg.read(opts.config)

    update = {
        'DEBUG': opts.debug
    }

    update['SHANNON_SERVER_IMAGE_ROOT'] = cfg.get('shannon_server', 'image_root')

    app.config.update(**update)
    app.run()
