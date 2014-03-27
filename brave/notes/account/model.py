from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, EmailField, DateTimeField, BooleanField, ReferenceField
from brave.notes.util.field import IPAddressField
from datetime import datetime, timedelta
from brave.api.client import API

from binascii import unhexlify
from hashlib import sha256
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import NIST256p

class Entity(EmbeddedDocument):
    meta = dict(allow_inheritance=False)
    
    id = IntField(db_field='i')
    name = StringField(db_field='n')

class User(Document):
    meta = dict(
        collection = 'Users',
        allow_inheritance = False,
        indexes = [
            'character.id'
        ],
    )
    
    token = StringField(db_field='t')

    character = EmbeddedDocumentField(Entity, db_field='c', default=lambda: Entity())
    corporation = EmbeddedDocumentField(Entity, db_field='o', default=lambda: Entity())
    alliance = EmbeddedDocumentField(Entity, db_field='a', default=lambda: Entity())

    expires = DateTimeField(db_field='e')
    seen = DateTimeField(db_field='s')

    @property
    def attempts(self):
        return LoginHistory.objects(user=self)

    @classmethod
    def authenticate(self, identifier, password=None):
        """Validate the given identifier; password is ignored."""
        from brave.notes.config import settings
        try:
            private = SigningKey.from_string(unhexlify(settings['api']['private']), curve=NIST256p, hashfunc=sha256)
            public = VerifyingKey.from_string(unhexlify(settings['api']['public']), curve=NIST256p, hashfunc=sha256)
        except:
            return "Invalid keys"

        api = API(settings['api']['endpoint'], settings['api']['identity'], private, public)
        result = api.core.info(identifier)
        
        user = self.objects(character__id=result.character.id).first()
        
        if not user:
            user = self(token=identifier, expires=result.expires, seen=datetime.utcnow())
            user.character.id = result.character.id
            user.character.name = result.character.name
            user.corporation.id = result.corporation.id
            user.corporation.name = result.corporation.name
            
            if result.alliance:
                user.alliance.id = result.alliance.id
                user.alliance.name = result.alliance.name
            
            user.save()
        
        else:
            # TODO: Also update the corporate details, if appropriate.
            user.update(set__token=identifier, set__seen=datetime.utcnow())
        
        from brave.notes.core.session import session
        session.user = user
        session.signedin = 1
        
        return user.id, user

class LoginHistory(Document):
    meta = dict(
            collection = "AuthHistory",
            allow_inheritance = False,
            indexes = [
                    'user',
                    # Automatically delete records as they expire.
                    dict(fields=['expires'], expireAfterSeconds=0)
                ]
        )
    
    user = ReferenceField(User)
    success = BooleanField(db_field='s', default=True)
    location = IPAddressField(db_field='l')
    expires = DateTimeField(db_field='e', default=lambda: datetime.utcnow() + timedelta(days=365))