#!/bin/sh

apt-get install python-setuptools

sudo easy_install flask
sudo easy_install flask-cors

sudo apt-get install python-gevent
sudo apt-get install gunicorn

