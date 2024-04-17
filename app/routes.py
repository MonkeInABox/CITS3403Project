from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostNewPost
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post
from urllib.parse import urlsplit
from datetime import datetime, timezone

# What to do before calling anything else
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

# Landing Page
@app.route('/', methods=['GET'])
def index():
    '''Main landing page'''
    query = sa.select(Post)
    posts = db.session.scalars(query).all()

    return render_template('index.html', title='Home', posts=posts)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    form = PostNewPost()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user, category="Music")
        db.session.add(post)
        db.session.commit()
        flash("Congrats! New post")
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('new_post.html', form=form)

# Categories (can split if need be later on)
@app.route('/categories/', defaults={'category': None}, methods=['GET'])
@app.route('/categories/<category>/', methods=['GET'])
def categories(category):
    '''Categories page'''
    if category == None:
        return "Select a category"
    elif category != "":
        return f"welcome to the category {category}"

# NEED TO REWORK BELOW FUNCTIONALITY - IT IS VERY VERY BAD AND BROKEN!!!!
# Main profile page - maybe use cookies?? Need a sign in page probs /profile/signin?
@app.route('/profile/', defaults={'username': None}, methods=['GET'])
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    '''Profile page'''
    # If current user is attempting to access their own profile (without specifing in URL)
    if username == None and current_user.is_authenticated:
        print("test")
        user = db.first_or_404(sa.select(User).where(User.username == current_user))
        return render_template('profile.html', user=user)
    # If current user is attempting to access their own profile (with specifing in URL)
    elif current_user.is_authenticated:
        user = db.first_or_404(sa.select(User).where(User.username == username))
        return render_template('profile.html', user=user)
    # If someone is trying to see someone elses profile.
    elif username != current_user and username != None:
        user = db.first_or_404(sa.select(User).where(User.username == username))
        return render_template('profile.html', user=user)
    # If someone is trying to access their profile but isn't authenticated
    elif username == None and not current_user.is_authenticated:
        return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        # Get user from database
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        # If user exists in database (so the user object isn't empty) check password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('profile', username=current_user.username))
    return render_template('registration.html', title='Register', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


    