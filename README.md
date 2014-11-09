# plumbing-shannon-server

## Endpoints

	python ./flask/server.py -c server.cfg
	INFO:werkzeug: * Running on http://127.0.0.1:5000/

### /ping 

	curl 'http://localhost:5000/ping'
	{
		"stat": "ok"
	}

### /entropy

	# curl -X POST -F 'file=@/tmp/test.jpg' 'http://localhost:5000/entropy'

	curl 'http://localhost:5000/entropy?file=test.png'

	{
		"entropy": 9.386720101697886, 
	}

### /focalpoint

	# curl -X POST -F 'file=@/tmp/test.jpg' 'http://localhost:5000/focalpoint'

	curl 'http://localhost:5000/focalpoint?file=test.png'

	{
		"entropy": 9.386720101697886, 
		"h": 480, 
		"w": 640, 
		"x": 100, 
		"y": 180
	}

## Config

`plumbing-shannon-server` uses utility functions exported by the
[cooperhewitt.flask.http_pony](https://github.com/cooperhewitt/py-cooperhewitt-flask/blob/master/cooperhewitt/flask/http_pony.py)
library which checks your Flask application's configuration for details about
how to handle things.

The following settings should be added to a standard [ini style configutation
file](https://en.wikipedia.org/wiki/INI_file) in an `http_pony` section.

### http_pony

#### local_path_root

If set then files sent using an `HTTP GET` parameter will be limited to only
those that are are parented by this directory.

If it is not set then `HTTP GET` requests will fail.

#### upload_path_root

If set then files sent as an `HTTP POST` request will be first written to this
directory before processing.

If not set then the operating system's temporary directory will be used.

#### allowed_extensions

A comma-separate list of valid file extensions for processing.

## To do:

* Better documentation
* A proper `setup.py` file
