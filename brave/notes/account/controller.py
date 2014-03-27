import web
from web import form
from brave.notes.core.render import render
from brave.notes.account.model import User
from brave.notes.core.decorator import login_required, guest_required
from brave.notes.config import settings

from binascii import unhexlify
from hashlib import sha256
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import NIST256p

from brave.api.client import API

urls = (
    '/authorize', 'authorize',
    '/authorized', 'authorized',
    '/signout', 'signout',
)

@guest_required
class authorize:

    def GET(self):

        try:
            private = SigningKey.from_string(unhexlify(settings['api']['private']), curve=NIST256p, hashfunc=sha256)
            public = VerifyingKey.from_string(unhexlify(settings['api']['public']), curve=NIST256p, hashfunc=sha256)
        except:
            return "Invalid keys"
        # Perform the initial API call and direct the user.
        api = API(settings['api']['endpoint'], settings['api']['identity'], private, public)

        success = str(settings['domain'] + settings['path'] + '/account/authorized')
        failure = str(settings['domain'] + settings['path'] + '/account/nolove')

        result = api.core.authorize(success=success, failure=failure)

        raise web.seeother(result.location, absolute=True)

@guest_required    
class authorized:

    def GET(self):
        # Perform the initial API call and direct the user.
        params  = web.input()

        User.authenticate(params.token)
        raise web.seeother(params.redirect if hasattr(params, 'redirect') else settings['path'] + "/notes", absolute=True)

@login_required
class switch:

    def GET(self):
        from brave.notes.core.session import session
        session.kill()
        
        try:
            private = SigningKey.from_string(unhexlify(settings['api']['private']), curve=NIST256p, hashfunc=sha256)
            public = VerifyingKey.from_string(unhexlify(settings['api']['public']), curve=NIST256p, hashfunc=sha256)
        except:
            return "Invalid keys"
        # Perform the initial API call and direct the user.
        api = API(settings['api']['endpoint'], settings['api']['identity'], private, public)

        success = str(settings['domain'] + settings['path'] + '/account/authorized')
        failure = str(settings['domain'] + settings['path'] + '/account/nolove')

        result = api.core.authorize(success=success, failure=failure)

        raise web.seeother(result.location, absolute=True)

@login_required
class signout:

    def GET(self):
        from brave.notes.core.session import session
        session.kill()
        raise web.seeother(settings['path'] + '/', absolute=True)

app_account = web.application( urls, locals() )