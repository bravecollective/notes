import web
from web import form
from brave.notes.core.render import render
from brave.notes.core.decorator import login_required
from brave.notes.notes.model import Category, Note
from brave.notes.config import settings
from brave.notes.util.formvalidation import body_validator, id_validator, title_validator, catid_validator

urls = (
    '/view/(.*)', 'view',
    '/edit/(.*)', 'edit',
    '/add', 'add',
    '/delete', 'delete',
    '/', 'notes',
    '', 'notes',
)

@login_required
class notes:
    def GET(self):
        from brave.notes.core.session import session
        return render.notes(Category.objects.GetCategories(session.user), None)

@login_required
class view:
    def GET(self, _id):
        if len(_id) != 24:
            raise web.notfound()

        from brave.notes.core.session import session
        note = Category.objects.GetNote(_id, session.user)

        if note == None:
            raise web.notfound()

        return render.notes(Category.objects.GetCategories(session.user), note)

@login_required
class edit:

    form = form.Form(
        form.Textbox('body', body_validator),
    )

    def GET(self, _id):
        if len(_id) != 24:
            raise web.notfound()
        from brave.notes.core.session import session

        return render.editnote(Category.objects.GetCategories(session.user), Category.objects.GetNote(_id, session.user), "")

    def POST(self, _id):
        if len(_id) != 24:
            raise web.notfound()
        from brave.notes.core.session import session
        form = self.form()
        error = ""
        if form.validates():
            body = form['body'].value

            c = Category.objects.GetNoteCategory(_id, session.user)
            c[0].notes[c[1]].text = body
            c[0].save()
            raise web.seeother(settings['path'] + '/notes/view/' + _id, absolute=True)
        else:
            for k in form.inputs:
                if k.note != None:
                    error = k.note
                    break

        return render.editnote(Category.objects.GetCategories(session.user), Category.objects.GetNote(_id, session.user), error)

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
        error = ""
        if form.validates():
            _id = form['id'].value
            if len(_id) != 24:
                raise web.notfound()

            c = Category.objects.GetNoteCategory(_id, session.user)
            c[0].notes.pop(c[1])
            c[0].save()
            raise web.seeother(settings['path'] + '/notes', absolute=True)
        else:
            for k in form.inputs:
                if k.note != None:
                    error = k.note
                    break

        return render.editnote(Category.objects.GetCategories(session.user), Category.objects.GetNote(_id, session.user), error)

@login_required
class add:

    form = form.Form(
        form.Textbox('category', catid_validator),
        form.Textbox('title', title_validator),
        form.Textbox('body', body_validator),
    )

    def GET(self):
        from brave.notes.core.session import session
        return render.addnote(Category.objects.GetCategories(session.user), "")

    def POST(self):
        from brave.notes.core.session import session
        form = self.form()
        error = ""
        if form.validates():
            title = form['title'].value
            body = form['body'].value
            category = form['category'].value

            query = dict(user=session.user)
            query[b'id'] = category
            cat = Category.objects(**query).first()
            
            if cat:
                found = False
                for note in cat.notes:
                    if note.title == title:
                        found = True
                        break

                if not found:
                    note = Note()
                    note.title = title
                    note.text = body
                    cat.notes.append(note)
                    cat.save()
                    raise web.seeother(settings['path'] + '/notes/view/' + str(note.nid), absolute=True)
                else:
                    error = "Title already exists"
            else:
                error = "Category does not exist!"
        else:
            for k in form.inputs:
                if k.note != None:
                    error = k.note
                    break

        return render.addnote(Category.objects.GetCategories(session.user), error)

app_notes = web.application( urls, locals() )