from __future__ import unicode_literals

import web

from time import time, sleep
from datetime import datetime
from brave.notes.account.model import User, LoginHistory

def authenticate(email, password):
    
    ts = time() # Record the
    query = dict(active=True)
    
    # Gracefully handle extended characters in passwords.
    # The password storage algorithm works in binary.
    if isinstance(password, unicode):
        password = password.encode('utf8')
    
    # Build the MongoEngine query to find
    query[b'email'] = email
    
    user = User.objects(**query).first()
    
    if not user or not User.password.check(user.password, password):
        if user:
            LoginHistory(user, False, web.ctx['ip']).save()
        
        # Prevent basic timing attacks; always take at least one second to process.
        sleep(max(min(1 - (time() - ts), 0), 1))
        
        return None
    
    # Record the fact the user signed in.
    LoginHistory(user, True, web.ctx['ip']).save()
    
    return user.id, user