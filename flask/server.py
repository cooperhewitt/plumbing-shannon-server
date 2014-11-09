#!/usr/bin/env python

import os
import os.path
import logging

import flask
from flask_cors import cross_origin 

import Image

try:
    # https://github.com/cooperhewitt/py-cooperhewitt-roboteyes-shannon
    import cooperhewitt.roboteyes.shannon as shannon
except Exception, e:
    import shannon

try:
    # https://github.com/cooperhewitt/py-cooperhewitt-flask
    import cooperhewitt.flask.http_pony as http_pony
except Exception, e:
    import http_pony

app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
@cross_origin(methods=['GET'])
def ping():

    return flask.jsonify({'stat': 'ok'})

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
        path = http_pony.get_upload_path(app)
    else:
        path = http_pony.get_local_path(app)

    try:
        if flask.request.method=='POST':
            path = http_pony.get_upload_path(app)
        else:
            path = http_pony.get_local_path(app)

    except Exception, e:
        logging.error(e)
        flask.abort(400)

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
        logging.debug("unlink %s" % path)
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
    parser.add_option("-v", "--verbose", dest="verbose", help="enable chatty logging; default is false", action="store_true", default=False)

    opts, args = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("verbose logging is enabled")
    else:
        logging.basicConfig(level=logging.INFO)

    cfg = ConfigParser.ConfigParser()
    cfg.read(opts.config)

    http_pony.update_app_config(app, cfg)

    app.run()
