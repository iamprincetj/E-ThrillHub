from mongoengine import *
from flask_login import UserMixin
import certifi

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")


ca = certifi.where()

#uri = "mongodb+srv://princetj:wAvxiXqXUgJP9vH7@justincluster0.pvvyuo6.mongodb.net/sample_airbnb?retryWrites=true&ssl=true&w=majority"
uri = f"mongodb+srv://{db_username}:{db_password}@alxportfolio1.rfv02wi.mongodb.net/JustIN_project?retryWrites=true&ssl=true&w=majority"

con = connect(host=uri, tlsCAFile=ca)
db = con.JustIN_project
#con = connect("tumblelog")
#db = con.tumblelog


class Comments(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


class User(Document, UserMixin):
    email = StringField(required=True)
    username = StringField()
    password = StringField()
    profile_pic = StringField()
    changed_profile_pic = FileField()

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

