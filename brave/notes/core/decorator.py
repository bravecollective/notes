import web
from functools import wraps
from brave.notes.config import settings

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kw):
        from brave.notes.core.session import session
        if session.signedin == 1:
            return f(*args, **kw)
        else:
            raise web.seeother(settings['path'] + '/', absolute=True)
    return wrapper

def guest_required(f):
    @wraps(f)
    def wrapper(*args, **kw):
        from brave.notes.core.session import session
        if session.signedin == 0:
            return f(*args, **kw)
        else:
            raise web.seeother(settings['path'] + '/notes', absolute=True)
    return wrapper