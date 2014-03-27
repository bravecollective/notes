import web
from web import form
from brave.notes.core.render import render
from brave.notes.core.decorator import login_required
from brave.notes.notes.model import Category, Note
from brave.notes.util.formvalidation import id_validator, name_validator
from brave.notes.config import settings

urls = (
    '/add', 'add',
    '/delete', 'delete',
    '/', 'categories',
    '', 'categories',
)

@login_required
class categories:
    def GET(self):
        from brave.notes.core.session import session
        return render.categories(Category.objects.GetCategories(session.user), None)

@login_required
class add:

    form = form.Form(
        form.Textbox('category', name_validator),
    )

    def GET(self):
        from brave.notes.core.session import session
        return render.addcategory(Category.objects.GetCategories(session.user), "")

    def POST(self):
        from brave.notes.core.session import session
        form = self.form()
        error = ""
        if form.validates():
            category = form['category'].value
            
            query = dict(user=session.user)
            query[b'title'] = category
            cat = Category.objects(**query).first()
            
            if not cat:
                cat = Category(session.user, category)
                cat.save()
                raise web.seeother(settings['path'] + '/categories', absolute=True)
            else:
                error = "Category already exists!"
        else:
            for k in form.inputs:
                if k.note != None:
                    error = k.note
                    break

        return render.addcategory(Category.objects.GetCategories(session.user), error)

@login_required
class delete:

    form = form.Form(
        form.Textbox('id', id_validator),
    )

    def GET(self):
        raise web.notfound()

    def POST(self):
        from brave.notes.core.session import session
        form = self.form()

        if form.validates():
            _id = form['id'].value            
            c = Category.objects(**dict(id = _id)).first()
            if c:
                c.delete()
        else:
            for k in form.inputs:
                if k.note != None:
                    return k.note

        raise web.seeother(settings['path'] + '/categories', absolute=True)

app_categories = web.application( urls, locals() )