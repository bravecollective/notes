1. What is BravePad
-----

Coming soon...

2. Installation
------
Before you start, python 2.7, MongoDB and virtualenv is required.  
Start by creating a python environment

    virtualenv bravenotes

After that

    cd bravenotes
    source bin/activate
	git clone https://github.com/bravecollective/api.git
    (cd api; python setup.py develop)
	
    git clone https://github.com/bravecollective/notes.git

Copy the sample config and modify it to your preference  
``(cd bravenotes/brave/notes; cp config.py.sample config.py; editor config.py)``

    
Development:
Start application by running the following commands

    cd bravenotes/app
    python __init__.py
    
Live:

    sudo apt-get install spawn-fcgi

Modify the first line in fcgi.py to be the path to the virtualenv python binary.
Modify the path in the init script ("service" file in root) to match your installation and save it to ``/etc/init.d/bravenotes`` and make it runable ``chmod +x /etc/init.d/bravenotes``
Make fcgi.py runable ``chmod +x fcgi.py``

Make the site autostart ``sudo update-rc.d bravenotes defaults``

Add the code below to your nginx site config file and modiy the path to the static content.

    location / {
        fastcgi_param REQUEST_METHOD $request_method;
        fastcgi_param QUERY_STRING $query_string;
        fastcgi_param CONTENT_TYPE $content_type;
        fastcgi_param CONTENT_LENGTH $content_length;
        fastcgi_param GATEWAY_INTERFACE CGI/1.1;
        fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;
        fastcgi_param REMOTE_ADDR $remote_addr;
        fastcgi_param REMOTE_PORT $remote_port;
        fastcgi_param SERVER_ADDR $server_addr;
        fastcgi_param SERVER_PORT $server_port;
        fastcgi_param SERVER_NAME $server_name;
        fastcgi_param SERVER_PROTOCOL $server_protocol;
        fastcgi_param SCRIPT_FILENAME $fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_pass 127.0.0.1:9002;
    }

    location /static {
        alias /path/to/static/;
    }
    
Start the site ``sudo service notepad start``