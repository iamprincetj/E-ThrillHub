from mongoengine import *
from flask_login import UserMixin

connect('tumblelog')

class Comments(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


class User(Document, UserMixin):
    email = StringField(required=True)
    username = StringField()
    password = StringField()

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comments))

    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = FileField()

class LinkPost(Post):
    link_url = StringField()