#!/usr/bin/env python

import os
import os.path

import flask
from flask_cors import cross_origin 
from werkzeug.security import safe_join

import shannon
import Image

import logging

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
        safe = safe_join(root, path)

        if not safe:
            logging.error("'%s' + '%s' considered harmful" % (root, path))
            flask.abort(400)

        path = safe

    logging.debug("final request path is %s" % path)
    
    if not os.path.exists(path):
        logging.error("%s does not exist" % path)
        flask.abort(404)

    return path

@app.route('/ping', methods=['GET'])
@cross_origin(methods=['GET'])
def ping():
    rsp = {'stat': 'ok'}
    return flask.jsonify(**rsp)

@app.route('/entropy', methods=['GET'])
@cross_origin(methods=['GET'])
def entropy():

    path = get_path()
    return _entropy(path)

    return flask.jsonify(entropy=rsp)

@app.route('/focalpoint', methods=['GET'])
@cross_origin(methods=['GET'])
def focalpoint():

    path = get_path()
    rsp = _focalpoint(path)

    return flask.jsonify(**rsp)

def _entropy(path):
    im = Image.open(path)
    return shannon.entropy(im)

def _focalpoint(path):
    im = Image.open(path)
    return shannon.focalpoint(im)
    
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
