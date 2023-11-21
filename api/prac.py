from mongoengine import connect
from models import User, Post, ImagePost
from flask import Flask
import json
from bson.objectid import ObjectId
from gridfs import GridFS

from flask_login import LoginManager

app = Flask(__name__)

posts = Post.objects()
for post in posts:
    print(post.image_path._id)

# Assuming you have the ImagePost's id
post_id = "655be0bea37509dbac28e5fb"

# Retrieve the ImagePost document from the database
img_post = ImagePost.objects(id=post_id).first()

# Access the image_path ObjectId
#image_id = img_post.image_path

image_id = img_post.image_path._id
print(image_id)
# # Retrieve the image from GridFS using the image_path ObjectId
# fs = GridFS()
# img = fs.get(ObjectId(image_id))


# def get_image(image_id):
#     connect('flask_mongoengine')
#     fs = GridFS()
#     img = fs.get(ObjectId(image_id))
#     return img.read()


