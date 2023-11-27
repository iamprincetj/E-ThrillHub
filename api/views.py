from hashlib import md5
from io import BytesIO
import ssl
from flask import Blueprint, render_template, redirect, request, flash, send_file, url_for, Response
from flask_login import current_user, login_required
from api.models import Post, TextPost, ImagePost, LinkPost, User, db
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS
import certifi


ca = certifi.where()

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@views.route('/news')
@login_required
def news():
    page = request.args.get('page', default=1, type=int)
    posts_per_page = 1
    offset = (page - 1) * posts_per_page
    post = Post.objects().skip(offset).limit(posts_per_page)
    post_len = len(Post.objects())
    return render_template('news.html', user=current_user, post=post, page=page, post_len=post_len)

@views.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        textpost = request.form.get('textpost')
        imagepost = request.form.get('imagepost')
        linkpost = request.form.get('linkpost')
        print(request.form)

        if textpost == 'on' and imagepost != 'on' and linkpost != 'on':
            return redirect(url_for('views.textpost'))
        elif imagepost == 'on' and linkpost != 'on' and textpost != 'on':
            return redirect(url_for('views.imagepost'))
        elif linkpost == 'on' and textpost != 'on' and imagepost != 'on':
            return redirect(url_for('views.linkpost'))
        else:
            flash('Must Select One Post Type', category='error')
    return render_template('post.html', user=current_user)

@views.route('/post/textpost', methods=['GET', 'POST'])
def textpost():
    if request.method == 'POST':
        user = User.objects(id=current_user.id).first()
        text = TextPost(author=user)
        text.content = request.form.get('content')
        text.title = request.form.get('title')
        text.save()
        flash('Post Created!', category='success')
    return render_template('textpost.html', user=current_user)

@views.route('/post/imagepost', methods=['GET', 'POST'])
def imagepost():
    if request.method == 'POST':
        user = User.objects(id=current_user.id).first()
        img = ImagePost(author=user)
        title = request.form.get('title')
        img.title = title
        file = request.files['imagepost'] 
        print(request.files['imagepost'])
        img.image_path.put(file)
        img.save()
        flash('Post Created!', category='success')
    return render_template('imagepost.html', user=current_user)

@views.route('/post/linkpost', methods=['GET', 'POST'])
def linkpost():
    if request.method == 'POST':
        user = User.objects(id=current_user.id).first()
        link = LinkPost(title='my first post', author=user)
        link.link_url = request.form.get('link_url')
        link.save()
        flash('Post Created!', category='success')
    return render_template('linkpost.html', user=current_user)

@views.route('/image/<image_id>')
def get_image(image_id):
    #print(db)  replace with your database name
    fs = GridFS(db)
    file_id = ObjectId(image_id)
    file = fs.get(file_id)
    response = Response(file.read(), mimetype='image/*')
    return response

@views.route('/images/<id>')
def serve_image(id):
    img = ImagePost.objects.with_id(id)
    return send_file(BytesIO(img.image_path.read()), mimetype='image/jpeg')

@views.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if request.method == "POST":
        new_username = request.form.get("change_username")
        new_profile_pic = request.files['change_profile_pic']
        if new_profile_pic:
            user = User.objects(username=username).first()
            if user.changed_profile_pic.read():
                user.changed_profile_pic.delete()
            user.changed_profile_pic.put(new_profile_pic)
            user.save()
            flash('Profile picture changed', category='success')
            return redirect(f'/profile/{username}')
        if new_username:
            exist_user = User.objects(username=new_username).first()
            if exist_user:
                flash('Username already taken, Try another', category='error')
            else:
                User.objects(username=username).update(username=new_username)
                flash('Username successfully changed', category='success')
                return redirect(f'/profile/{new_username}')

    user = User.objects(username=username).first()
    page = request.args.get('page', default=1, type=int)
    posts_per_page = 1
    offset = (page - 1) * posts_per_page
    post = Post.objects(author=user).skip(offset).limit(posts_per_page)
    post_len = len(Post.objects(author=user))
    return render_template('profile.html', user=current_user, post=post, page=page, post_len=post_len, searched_user=user)