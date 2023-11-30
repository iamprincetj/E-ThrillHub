'''from mongoengine import connect
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



from flask import request

@views.route('/news')
@login_required
def news():
    page = request.args.get('page', default=1, type=int)
    posts_per_page = 20
    offset = (page - 1) * posts_per_page
    posts = Post.objects().skip(offset).limit(posts_per_page)
    return render_template('news.html', user=current_user, post=posts)

'''

from hashlib import md5
email = 'tochukwunwanze5@gmail.com'

img = f'https://www.gravatar.com/avatar/{md5(email.encode("utf-8")).hexdigest()}?d=identicon&s=128'
print(img)