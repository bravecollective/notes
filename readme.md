## 1. What is Brave Notes?

Coming soon...

## 2. Installation

Before you start, python 2.7, MongoDB and virtualenv is required.  
Start by creating a python environment

    virtualenv bravenotes

After the virtual environment has been created, run the commands below:

    cd bravenotes
    source bin/activate
	git clone https://github.com/bravecollective/api.git
    (cd api; python setup.py develop)
    git clone https://github.com/bravecollective/notes.git
    (cd notes; python setup.py develop)

Copy the sample config and modify it to your preference  
``(cd notes/brave/notes; cp config.py.sample config.py; editor config.py)``

    
Development:

Start application by running the following commands

    cd notes
    python startup.py
    
Live:

    cd notes
    sudo apt-get install spawn-fcgi

Modify the first line in fcgi.py to be the path to the virtualenv python binary.
Modify the path in the init script ("service" file in root) to match your installation, save it and make the service autorun.

    (cp service /etc/init.d/bravenotes; sudo update-rc.d bravenotes defaults; editor /etc/init.d/bravenotes)

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

## 4. License
Brave Collective Notes has been released under the MIT Open Source license.  All contributors agree to transfer ownership of their code to Felix Gustavsson for release under this license.  (This is to mitigate issues in the future.)


### 4.1 The MIT License

Copyright (C) 2014 Felix Gustavsson and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
