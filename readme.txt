-- version: 1.0.1
-- python_vertion: 3.5.0
-- django_version: 1.11.5


[TOC]

### packages
#### yum packages
development tools, python3, nginx, memcached, mysql, mysql-server

#### pip packages
uwsgi, django, pymysql, pillow, six, djangorestframework


#### initial the system
**->(path base on the project root)**
1. bekazone/setting.py
`DEBUG = False` -> `DEBUG = True`
2. backup the `users/form.py` file and change the `users/form.py` by `users/form.py_bak`
3. the mysql message on the `etc/bekazone/config.ini`
```
python manage.py makemigrations
python manage.py migrate
```
4. reduce the `form.py`

### build a daemon server
server start and stop(redhat)
```
service nginx start/stop # service (name) start/stop/restart/reload
mysqld, uwsgi
```

server boot start
```
chkconfig nginx on # chkconfig (name) on/off
```

config a daemon server
path: /etc/systemd/system/
```
[Unit]
Description=uWSGI instance to serve myapp

[Service]
ExecStartPre=/usr/bin/bash -c 'mkdir -p /var/log/uwsgi; chown nginx:nginx /var/log/uwsgi; mkdir -p /var/run/uwsgi; chown nginx:nginx /var/run/uwsgi'
ExecStart=/usr/bin/bash -c 'cd /usr/local/bekazone; uwsgi bekazone_uwsgi.ini'

[Install]
WantedBy=multi-user.target
```


### configurations
#### uwsgi.ini
```
[uwsgi]
socket = 0.0.0.0:3000
chdir = /usr/local/bekazone
chmod-socket = 666
#home = /usr/local/python/lib/python3.6
pythonpath = /usr/local/python/lib/python3.6
wsgi-file = bekazone/wsgi.py
processes = 4
threads = 25
master = true
#attach-daemon = memcached -p 11211 -u nginx
logger = file:/tmp/errlog
#stats = 127.0.0.1:9191
pidfile = /var/run/uwsgi/uwsgi.pid
daemonize=/var/log/uwsgi/%n.log
vacuum=true
module=wsgi:application
uid=nginx
gid=nginx
enable-threads = true
max-requests = 1000
max-worker-lifetime = 3600
reload-on-rss = 2048
worker-reload-mercy = 60
```

run the uwsgi server:
`uwsgi uwsgi.ini`

**the fundament configuration**
select project path: chdir, wsgi-file
socket: http, socket, http-socket

*have two aspect on the socket configuration
```
socket = 0.0.0.0:3000 # give a address or
socket = /tmp/%n.sock # give a socket file
```


**daemonize**
logger, daemonize

**config for performance:**
enable-threads, threads, processes
max-requests, max-worker-lifetime, reload-on-rss, worker-reload-mercy
master


#### config http on nginx
config with normal port
```
server {
    listen       80;
   　server_name  localhost;
   　location / {
		include        uwsgi_params;
		uwsgi_pass 127.0.0.1:3000;　　# uwsgi port, or a socket path: unix:///tmp/project.socket
    }
	
	location /static {
		alias /usr/local/bekazone/static;
	}
	
	#error_page  404              /404.html;
	error_page   500 502 503 504 =500 /pages-500.html;
    location = /pages-500.html {
		root   /usr/local/bekazone/templates/;
	}
}
```


config with ssl port on nginx

```
server {
    listen       443 ssl;
    server_name  localhost;

	ssl_certificate     /etc/nginx/ssl/server.crt;
	ssl_certificate_key /etc/nginx/ssl/server.key;

    ssl_session_cache    shared:SSL:1m;
    ssl_session_timeout  5m;

    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers  on;
    location / {
	    include        uwsgi_params;
		uwsgi_pass 127.0.0.1:3000;
	}
	error_page   500 502 503 504 =500 /pages-500.html;
	    location = /pages-500.html {
		root   /usr/local/bekazone/templates/;
	}
    location /static {
		alias /usr/local/bekazone/static;
	}
}
```


