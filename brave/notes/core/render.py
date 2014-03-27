import web
import markdown
from brave.notes.config import p_globals

py_globals = p_globals.copy()
py_globals['session'] = lambda: web.ctx.session
py_globals['render'] = web.template.render('brave/notes/templates/', globals=p_globals)
py_globals['md'] = markdown.Markdown(safe_mode='replace', html_replacement_text='--RAW HTML NOT ALLOWED--')

render = web.template.render('brave/notes/templates/', base='master', globals=py_globals)