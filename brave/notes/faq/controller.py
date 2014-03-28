import web
from brave.notes.core.render import render
from brave.notes.core.decorator import login_required

urls = (
	'', 'faq'
)

@login_required
class faq:
    def GET(self):
        return render.faq()

app_faq = web.application( urls, locals() )