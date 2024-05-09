from flask import render_template, flash, redirect, url_for, request, current_app
from app.main.forms import EditProfileForm, PostNewComment, SearchForm
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
@bp.route('/', methods=['GET', 'POST'])
def index():
    '''Main landing page'''
    comment_form = PostNewComment()

    if comment_form.validate_on_submit() and current_user.is_authenticated:
        # Create a new comment and associate it with the correct post
        post_id = request.form.get('post_id')
        print(f"post id: {post_id}")

        post = Post.query.get(post_id)
        if post:
            new_comment = Comment(body=comment_form.body.data, post_id=post_id, author_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()

    # Handle pagination and query for posts as usual
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

    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url, comment_form=comment_form)

# Main profile page
@bp.route('/profile/', defaults={'username': None}, methods=['GET'])
@bp.route('/profile/<username>', methods=['GET'])
def profile(username):
    '''Profile page'''

    # Get page number from query string or default to 1
    page = request.args.get('page', 1, type=int)

    # If username is None, assume the user is accessing their own profile
    if username is None:
        # If the user is authenticated, load their profile
        if current_user.is_authenticated:
            user = current_user
        else:
            # If not authenticated, redirect to register
            return redirect(url_for('register'))
    else:
        # If a username is provided, load that user's profile
        user = db.first_or_404(sa.select(User).where(User.username == username))

    # Query posts for the user
    query = sa.select(Post).filter(Post.author == user).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    # Generate next and previous page URLs
    next_url = url_for('main.profile', username=username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.profile', username=username, page=posts.prev_num) if posts.has_prev else None

    # Render the profile page with user information and posts
    return render_template('profile.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

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

@bp.context_processor
def heading():
    form = SearchForm()
    return dict(form=form)

#Search Page
@bp.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.searched.data
    page = request.args.get('page', 1, type=int)

    query = sa.select(Post).filter(Post.body.like('%' + search_term + '%')).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    if posts.has_next:
        next_url = url_for('main.search', page=posts.next_num)
    else:
        next_url = None

    if posts.has_prev:
        prev_url = url_for('main.search', page=posts.prev_num)
    else:
        prev_url = None

    return render_template('search.html', title='Search', form = form, search_term = search_term, posts = posts.items, next_url = next_url, prev_url = prev_url)