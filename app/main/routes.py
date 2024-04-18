from flask import render_template, flash, redirect, url_for, request, current_app
from app.main.forms import EditProfileForm, PostNewPost
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import User, Post, Comment
from datetime import datetime, timezone
from app.main import bp
from app import db

# What to do before calling anything else
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

# Landing Page
@bp.route('/', methods=['GET'])
def index():
    '''Main landing page'''
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)
    else:
        next_url = None

    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)
    else:
        prev_url = None

    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    form = PostNewPost()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user, category="Music")
        db.session.add(post)
        db.session.commit()
        flash("Congrats! New post")
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        return render_template('new_post.html', form=form)

# Categories (can split if need be later on)
@bp.route('/categories/', defaults={'category': None}, methods=['GET'])
@bp.route('/categories/<category>/', methods=['GET'])
def categories(category):
    '''Categories page'''
    if category == None:
        return "Select a category"
    elif category != "":
        return f"welcome to the category {category}"

# NEED TO REWORK BELOW FUNCTIONALITY - IT IS VERY VERY BAD AND BROKEN!!!!
# Main profile page - maybe use cookies?? Need a sign in page probs /profile/signin?
@bp.route('/profile/', defaults={'username': None}, methods=['GET'])
@bp.route('/profile/<username>', methods=['GET'])
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

@bp.route('/edit_profile', methods=['GET', 'POST'])
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


    