import web
from brave.notes.core.render import render
from brave.notes.core.decorator import guest_required

urls = (
	'', 'home'
)

@guest_required
class home:
    def GET(self):
        return render.home()

app_home = web.application( urls, locals() )