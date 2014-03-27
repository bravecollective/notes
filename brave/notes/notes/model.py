from mongoengine import QuerySet, Document, EmbeddedDocument, ObjectIdField, StringField, EmbeddedDocumentField, ListField, ReferenceField
from brave.notes.account.model import User
import bson

class CategoryQuerySet(QuerySet):
    def GetNote(document, _id, u = None):
        query = dict(user=u)
        query[b'notes__nid'] = _id
        notes = Category.objects(**query).first()
        if notes == None:
            return None
        
        for x in notes.notes:
            if str(x.nid) == str(_id):
                return x
        return None

    def GetNoteCategory(document, _id, u = None):
        query = dict(user=u)
        query[b'notes__nid'] = _id
        category = Category.objects(**query).first()
        if category == None:
            return None
        
        i = 0
        for x in category.notes:
            if str(x.nid) == str(_id):
                return category, i
            i += 1
        return None

    def GetCategories(document, u = None):
        query = dict(user=u)
        return Category.objects(**query).order_by('title')

class Note(EmbeddedDocument):
    nid = ObjectIdField(primary_key=True, default=lambda: bson.ObjectId())
    title = StringField(db_field='t')
    text = StringField(db_field='b')

class Category(Document):
    meta = dict(
        collection = 'Categories',
        allow_inheritance = False,
        queryset_class = CategoryQuerySet,
    )
    
    # Field Definitions
    user = ReferenceField(User)
    title = StringField(db_field='t', required=True)
    notes = ListField(EmbeddedDocumentField(Note), db_field='ns')