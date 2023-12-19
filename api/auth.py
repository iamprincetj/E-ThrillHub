from hashlib import md5
from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required, logout_user
from api.models import User, Post

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(request.form)
        user = User.objects(email=email).first()
        print(user)
        if request.form.get('remember_me'):
            remember = True
        else:
            remember = False
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully', category='success')
                print(remember)
                login_user(user, remember=remember)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash("User with that email doesn't exist", category='error')
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template("log.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = User.objects(email=email).first()
        check_username = User.objects(username=username).first()
        if user:
            flash('User with this email already exists', category='error')
        elif check_username:
            flash('Username taken, try another', category='error')
        elif len(email) < 8 or email == "":
            flash('Invalid Email', category='error')
        elif len(username) < 2:
            flash('Username too short', category='error')
        elif len(password) < 8:
            flash('password must be greater than 7 characters', category='error')
        elif confirm_password != password:
            flash("passwords don't match")
        else:
            img = f'https://www.gravatar.com/avatar/{md5(email.encode("utf-8")).hexdigest()}?d=identicon&s=128'
            user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), profile_pic=img)
            user.save()
            flash('Account Created')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template('sign.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    User.delete(current_user)
    flash('successfully delete your account')
    return redirect(url_for('auth.login'))