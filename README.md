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

### http_pony

#### local_path_root

#### upload_path_root

#### allowed_extensions

## To do:

* Better documentation
* A proper `setup.py` file
