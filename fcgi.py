#!/home/blackvoid/bravenotes/bin/python
from startup import app
import web

web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
app.run()
