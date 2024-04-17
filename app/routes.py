from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit

# Landing Page
@app.route('/', methods=['GET', 'POST'])
def index():
    '''Main landing page'''
    # if flask.request.method == POST
    #    handleUserPost(flask.request.values.get('postText'))
    #
    #  This would just handle when users want to submit things to the board?

    user = {'username': 'Miguel'}
    
    return render_template('index.html', title='Home')

# Categories (can split if need be later on)
@app.route('/categories/', defaults={'category': None}, methods=['GET'])
@app.route('/categories/<category>/', methods=['GET'])
def categories(category):
    '''Categories page'''
    if category == None:
        return "Select a category"
    elif category != "":
        return f"welcome to the category {category}"
    
# Main profile page - maybe use cookies?? Need a sign in page probs /profile/signin?
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    '''Profile page'''
    # if signedInProfile == None:
    #    return redirect("https://www.127.0.0.1:5000/profile/signin")??? Maybe idk
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
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
        return redirect(url_for('profile'))
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
        return redirect(url_for('profile'))
    return render_template('registration.html', title='Register', form=form)

#@app.route('search/<searchedFor>', methods=['GET'])
#def search():
    '''Search Bar Functionality'''
    # Handle what ever it is that the search bar needs to handle - string matching etc.


    