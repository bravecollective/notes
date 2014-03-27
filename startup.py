import web, sys, os
import mongoengine
from brave.notes.core.render import render
from brave.notes.config import settings

from brave.notes.home.controller import app_home
from brave.notes.notes.controller import app_notes
from brave.notes.account.controller import app_account
from brave.notes.categories.controller import app_categories

mongoengine.connect('BraveNotes')

urls = (
    settings['path'] + '/notes', app_notes,
    settings['path'] + '/account', app_account,
    settings['path'] + '/categories', app_categories,
    settings['path'] + '/', app_home,
    settings['path'] + '', app_home,
)

app = web.application(urls, globals())

store = web.session.DiskStore('brave/notes/sessions')
session = web.session.Session(app,store,initializer={'signedin': 0, 'user': None})

def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

def notfound( message='The server cannot find the requested page.'):
    return web.notfound(render.notfound())
app.notfound = notfound

if __name__ == "__main__":
    app.run()
