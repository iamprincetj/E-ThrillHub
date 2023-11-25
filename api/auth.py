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
        user = User.objects(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash("User with that email doesn't exist", category='error')
    return render_template("login.html", user=current_user)

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
            user = User(email=email, username=username, password=generate_password_hash(password, method='scrypt'))
            user.save()
            flash('Account Created')
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))