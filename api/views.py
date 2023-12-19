from hashlib import md5
from io import BytesIO
import ssl
from flask import Blueprint, jsonify, render_template, redirect, request, flash, send_file, url_for, Response, session, abort
from flask_login import current_user, login_required
from api.models import Post, User, db, ImagePost, Comments
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS
import certifi


ca = certifi.where()

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', default=1, type=int)
    posts_per_page = 5
    offset = (page - 1) * posts_per_page
    posts = Post.objects().skip(offset).limit(posts_per_page).order_by('-timestamp')
    post_len = len(Post.objects())
    return render_template('index.html', user=current_user, post=posts, page=page, post_len=post_len, posts_per_page=posts_per_page)

@views.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    page = request.args.get('page', default=1, type=int)
    posts_per_page = 2
    offset = (page - 1) * posts_per_page
    posts = Post.objects().skip(offset).limit(posts_per_page).order_by('-timestamp')
    post_len = len(Post.objects())
    return render_template('news.html', user=current_user, post=posts, page=page, post_len=post_len, posts_per_page=posts_per_page)

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
    user = User.objects(username=username).first()
    if user:
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
        posts_per_page = 5
        offset = (page - 1) * posts_per_page
        post = Post.objects(author=user).skip(offset).limit(posts_per_page).order_by('-timestamp')
        post_len = len(Post.objects(author=user))
        return render_template('profile.html', user=current_user, post=post, page=page, post_len=post_len, searched_user=user)
    
    else:
        abort(404)

@views.route('/makepost', methods=['POST'])
def makepost():
    user = User.objects(id=current_user.id).first()
    title = request.form.get('title')
    link = request.form.get('linkpost')
    image = request.files.get('imagepost')
    post = Post(author=user)
    if len(title) == "":
        flash('title must not be empty, say something', category='error')
    post.title = title
    post.link_url = link
    if image.filename != "":
        post.image_path.put(image)
    post.save()
    print(title, link, image.filename, image.name, image.headers, image.mimetype, user.username)
    flash('Post Created!', category='success')
    return redirect(url_for('views.home'))


@views.route('/profile/<username>/Edit_Profile', methods=['GET', 'POST'])
def edit_profile(username):
    if request.method == "POST":
        user = current_user
        print(request.form)
        new_username = request.form.get('change_username')
        new_email = request.form.get('change_email')
        new_profile_pic = request.files.get('change_profile_pic')
        bio = request.form.get('bio')

        user_email = User.objects(email=new_email).first()
        user_username = User.objects(username=new_username).first()

        if user_email and new_email != user.email:
            flash('A user with that email already exists, try again', category='error')
        elif user_username and new_username != user.username:
            flash('A user with that username already exists, try again', category='error')
        else:
            if new_email != user.email:
                user.update(email=new_email)
                flash('Email updated successfully')
            if new_username != user.username:
                user.update(username=new_username)
                flash('Username updated successfully')
            if bio is not None:
                print(bio)
                user.update(bio=bio)
                flash('Bio updated successfully')
        return redirect(url_for("views.edit_profile", username=user.username))

    return render_template('editprofile.html', user=current_user)

@views.route('/like/<post_id>', methods=['POST', 'GET'])
def like_post(post_id):
    post = Post.objects(id=post_id).first()
    current_user_like = None
    for liker in post.likes:
        if liker == current_user:
            current_user_like = liker
            break
    
    if current_user_like:
        post.likes.remove(current_user_like)
        has_liked = "unliked"
    else:
        post.likes.append(current_user)
        has_liked = "liked"
    post.save()
    return jsonify({'has_liked': has_liked})

@views.route('/comment/<post_id>', methods=['POST', 'GET'])
def comment_post(post_id):
    post = Post.objects(id=post_id).first()
    if request.method == "POST":
        content = request.form.get("comments")
        comment = Comments()
        comment.commenter = current_user
        comment.content = content
        post.comments.append(comment)
        post.save()
        flash('Successfully dropped your comment', category='success')
        return redirect(url_for('views.home'))
    len_likes = len(post.likes)
    return render_template('post.html', pos=post, user=current_user, likes=len_likes)

@views.route("/edit_post/<post_id>", methods=['POST'])
def edit_post(post_id):
    post = Post.objects(id=post_id).first()
    newText = request.form.get("edit_post_text")
    if newText == "":
        flash('Please input a valid text', category='error')
    print(newText)
    return redirect(f'/profile/{current_user.username}')

@views.route("/change_profile_picture/<username>", methods=['POST'])
def change_profile_picture(username):
    if request.method == "POST":
        user = User.objects(username=username).first()
        new_profile_pic = request.files.get('changed_profile_pic')
        print(new_profile_pic, user.changed_profile_pic, request.files)
        if new_profile_pic:
            if user.changed_profile_pic.read():
                user.changed_profile_pic.delete()
            user.changed_profile_pic.put(new_profile_pic)
            user.save()
            flash('Profile picture changed', category='success')
            return redirect(f'/profile/{username}')
    return render_template('editprofile.html', user=current_user)