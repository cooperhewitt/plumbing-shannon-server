#!/usr/bin/env python

import os
import os.path

import flask
from flask_cors import cross_origin 
from werkzeug.security import safe_join

import shannon
import Image

import logging
logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)

# Quick. And dirty. To figure out:
# http://flask.pocoo.org/docs/config/
# https://github.com/mbr/flask-appconfig
# (20140602/straup)

if os.environ.get('SHANNON_SERVER_IMAGE_ROOT', None):
    app.config['SHANNON_SERVER_IMAGE_ROOT'] = os.environ['SHANNON_SERVER_IMAGE_ROOT']

def get_path():

    path = flask.request.args.get('path')
    logging.debug("request path is %s" % path)

    root = app.config.get('SHANNON_SERVER_IMAGE_ROOT', None)

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
    im = Image.open(path)

    rsp = shannon.entropy(im)
    return flask.jsonify(entropy=rsp)

@app.route('/focalpoint', methods=['GET'])
@cross_origin(methods=['GET'])
def focalpoint():

    path = get_path()
    im = Image.open(path)

    rsp = shannon.focalpoint(im)
    return flask.jsonify(**rsp)

if __name__ == '__main__':
    debug = True	# sudo make me a CLI option
    app.run(debug=debug)
