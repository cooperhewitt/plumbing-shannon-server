#!/usr/bin/env python

import flask
from flask_cors import cross_origin 

import shannon
import Image

import logging
logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)

@app.route('/entropy', methods=['GET'])
@cross_origin(methods=['GET'])
def entropy():

    path = flask.request.args.get('path')
    im = Image.open(path)

    rsp = shannon.entropy(im)
    return flask.jsonify(entropy=rsp)

@app.route('/focalpoint', methods=['GET'])
@cross_origin(methods=['GET'])
def focalpoint():

    path = flask.request.args.get('path')
    im = Image.open(path)

    rsp = shannon.focalpoint(im)
    return flask.jsonify(**rsp)

if __name__ == '__main__':
    debug = True	# sudo make me a CLI option
    app.run(debug=debug)
