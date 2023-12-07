from mongoengine import *
from flask_login import UserMixin
import certifi
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")


ca = certifi.where()

uri = f"mongodb+srv://{db_username}:{db_password}@alxportfolio1.rfv02wi.mongodb.net/JustIN_project?retryWrites=true&ssl=true&w=majority"

con = connect(host=uri, tlsCAFile=ca)
db = con.JustIN_project
#con = connect("tumblelog")
#db = con.tumblelog



class User(Document, UserMixin):
    email = StringField(required=True)
    username = StringField()
    password = StringField()
    profile_pic = StringField()
    changed_profile_pic = FileField()

class Comments(EmbeddedDocument):
    content = StringField()
    commenter = ReferenceField(User)
    likes = ListField(ReferenceField(User))
    timestamp = DateTimeField(default=datetime.utcnow)


class Post(Document):
    title = StringField(max_length=1000, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    image_path = FileField()
    link_url = StringField()
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comments))
    likes = ListField(ReferenceField(User))
    timestamp = DateTimeField(default=datetime.utcnow)

class ImagePost(Document):
    image_path = FileField()

