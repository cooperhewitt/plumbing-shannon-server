# Running shannon-server using init.d

## gunicorn

_This assumes a Unix/Linux system. The following instructions do not apply for OS X or Windows._

First create local copies of the sample config file (for gunicorn) and shell scripts (for init.d)

	$> cd init.d      
	$> cp gunicorn-shannon-server.cfg.example gunicorn-shannon-server.cfg
	$> cp gunicorn-shannon-server.sh.example gunicorn-shannon-server.sh

### gunicorn-shannon-server.cfg
 
You will need to update `gunicorn-shannon-server.cfg` with the relevant paths and other configurations specific to your setup. This is what the sample config file looks like:

	# http://gunicorn-docs.readthedocs.org/en/latest/configure.html#configuration-file

	import os
	import multiprocessing

	workers = multiprocessing.cpu_count() * 2 + 1
	worker_class = "egg:gunicorn#gevent"

	# Server configs - adjust to taste

	bind = '127.0.0.1:8228'
	chdir = '/usr/local/bin'
	user = 'www-data'

	# All other user-specific configs

	os.environ['SHANNON_SERVER_CONFIG'] = '/path/to/server.cfg'

See the part where you are assigning `os.environ['SHANNON_SERVER_CONFIG']` ? That's the config file [described in main README.md document](../README.md#config).

### gunicorn-shannon-server.sh

You will need to update `shannon-server.sh` to point to the correct path for the _gunicorn_ config file that you've just edited. The relevant bit is:

	SHANNON_SERVER_CONFIG='/usr/local/plumbing-shannon-server/init.d/gunicorn-shannon-server.cfg'

## init.d

Link your init.d shell script in to `/etc/init.d` and tell the operating system to make sure it runs when the machine starts up:

	$> sudo ln -s /usr/local/plumbing-shannon-server/init.d/gunicorn-shannon-server.sh /etc/init.d/gunicorn-shannon-server.sh
	$> sudo update-rc.d gunicorn-plumbing-shannon-server.sh defaults

You can run the server in debug-mode like:

	$> sudo /etc/init.d/gunicorn-shannon-server.sh debug

Otherwise all the usual `/etc/init.d` conventions apply:

	$> sudo /etc/init.d/gunicorn-shannon-server.sh start
	$> sudo /etc/init.d/gunicorn-shannon-server.sh stop
