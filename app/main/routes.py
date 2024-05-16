from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, render_template_string
from app.main.forms import EditProfileForm, SearchForm, Delete, FilterForm
from app.comments.forms import PostNewComment
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import User, Post, Comment, Like, Dislike
from datetime import datetime, timezone
from app.main import bp
from app import db

#Pass stuff to navbar
@bp.context_processor
def heading():
    form = SearchForm()
    return dict(form=form)

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
    filter_form = FilterForm()
    query = 0

    if comment_form.validate_on_submit() and current_user.is_authenticated:
        # Create a new comment and associate it with the correct post
        post_id = request.form.get('post_id')

        post = Post.query.get(post_id)
        if post:
            new_comment = Comment(body=comment_form.body.data, post_id=post_id, author_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
    elif not comment_form.validate_on_submit() and request.method == 'POST':
        return jsonify(errors=comment_form.errors), 400  # Return 400 if post not found

    filter_data = request.args.get('filter')
    if filter_data:
        query = build_query(filter_data)
    else:
        query = sa.select(Post).order_by(Post.timestamp.desc())

    print(type(query))     

    # Handle pagination and query for posts as usual
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)
    else:
        next_url = None

    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)
    else:
        prev_url = None

    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url, comment_form=comment_form, current_user=current_user, filter_form = filter_form)
    
@bp.route('/filter', methods=['POST'])
def filter_posts():
    filter_form = FilterForm(request.form)
    if filter_form.validate_on_submit():
        filter_data = filter_form.filter.data
        # Redirect with filter identifier in the URL
        return redirect(url_for('main.index', filter=filter_data))
    else:
        # Handle validation errors
        return redirect(url_for('main.index'))

def build_query(filter_data):
    if filter_data == "nwst":
        query = sa.select(Post).order_by(Post.timestamp.desc())
    elif filter_data == "ldst":
        query = sa.select(Post).order_by(Post.timestamp.asc())
    elif filter_data == "mslk":
        query = sa.select(Post).join(Post.likes).group_by(Post.id).order_by(db.func.count(Post.likes).desc())
    elif filter_data == "msdk":
        query = sa.select(Post).join(Post.dislikes).group_by(Post.id).order_by(db.func.count(Post.dislikes).desc())
    elif filter_data == "mscm":
        query = sa.select(Post).join(Post.comments).group_by(Post.id).order_by(db.func.count(Post.comments).desc())
    return query

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
    return render_template('profile.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url, username=username)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.profile', username=current_user.username))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

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

@bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    form = Delete()
    user = db.first_or_404(sa.select(User).where(User.id == user_id))
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash('User deleted', 'info')
        return redirect(url_for('main.index'))
    return render_template('delete_user.html', form=form, user=user)

@bp.route('/like/<post_id>/<like_type>/<medium>', methods=['POST'])
@login_required
def like_or_dislike(post_id, like_type, medium):
    if medium == "post":
        post = Post.query.filter_by(id = post_id).first()
        like = Like.query.filter_by(author_id = current_user.id, post_id = post_id).first()
        dislike = Dislike.query.filter_by(author_id = current_user.id, post_id = post_id).first()
    else:
        comment = Comment.query.filter_by(id = post_id).first()
        like = Like.query.filter_by(author_id = current_user.id, comment_id = post_id).first()
        dislike = Dislike.query.filter_by(author_id = current_user.id, comment_id = post_id).first()
    
    if like:
        db.session.delete(like)
    elif like_type == "like" and medium == "post":
        like = Like(author_id = current_user.id, post_id = post_id)
        db.session.add(like)
    elif like_type == "like" and medium == "comment":
        like = Like(author_id = current_user.id, comment_id = post_id)
        db.session.add(like)
    
    if dislike:
        db.session.delete(dislike)
    elif like_type == "dislike" and medium == "post":
        dislike = Dislike(author_id = current_user.id, post_id = post_id)
        db.session.add(dislike)
    elif like_type == "dislike" and medium == "comment":
        dislike = Dislike(author_id = current_user.id, comment_id = post_id)
        db.session.add(dislike)
    
    db.session.commit()

    
    if medium == "post":
        like_count = len(post.likes) - len(post.dislikes)
        return jsonify({"likes": like_count, "liked": current_user.id in map(lambda x: x.author_id, post.likes), "disliked": current_user.id in map(lambda x: x.author_id, post.dislikes)})
    like_count = len(comment.likes) - len(comment.dislikes)
    return jsonify({"likes": like_count, "liked": current_user.id in map(lambda x: x.author_id, comment.likes), "disliked": current_user.id in map(lambda x: x.author_id, comment.dislikes)})

# Define a route to fetch comments for a specific post
@bp.route('/get_comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    # Retrieve comments for the specified post (Replace this with your logic)
    post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
    comments = post.comments
    # Assuming comments are in HTML format, you can return them directly
    html_content = render_template_string("""
        {% for comment in comments %}
        <p>
        {% include '_comment.html' %}
        </p>
        {% endfor %}
        """,
        comments=comments
    )
    print(html_content)
    return html_content

@bp.route('/submit_comment/<int:post_id>', methods=['POST'])
def submit_comment(post_id):
    post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
    comment_form = PostNewComment(request.form)

    if comment_form.validate_on_submit() and current_user.is_authenticated:
        # Create a new comment and associate it with the correct post
        if post:
            new_comment = Comment(body=comment_form.body.data, post_id=post_id, author_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            return jsonify({'success': True}), 200  # Return success response
    return jsonify({'success': False}), 400  # Return success response
