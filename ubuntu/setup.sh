#!/bin/sh

apt-get install python-setuptools

sudo easy_install flask
sudo easy_install flask-cors

# Again, not strictly necessary but you'll probably
# install this sooner or later... (20140125/straup)

sudo apt-get install gunicorn
