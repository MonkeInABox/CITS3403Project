from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from app.posts.forms import PostNewPost
from app.main.forms import SearchForm, Delete
from app.main.routes import _handle_comments_and_filters
from app.comments.forms import PostNewComment
from flask_login import current_user, login_required
from app.models import Post, Comment
from app.posts import bp
from app import db
import sqlalchemy as sa

#Pass stuff to navbar
@bp.context_processor
def heading():
    form = SearchForm()
    return dict(form=form)
    

@bp.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostNewPost()
    if form.validate_on_submit():
        post = Post(body=form.body.data, category=form.category.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        flash("Congrats! New post")
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        return render_template('new_post.html', form=form)


# Categories (can split if need be later on)
@bp.route('/categories/', defaults={'category': None}, methods=['GET'])
@bp.route('/categories/<category>/', methods=['GET', 'POST'])
def categories(category):
    '''Categories page'''
    if category is None or category not in current_app.config['CATEGORIES']:
        return redirect(url_for('main.index'))

    result = _handle_comments_and_filters(current_app.config['CATEGORIES'][category])
    if isinstance(result, tuple) and result[1] == 400:
        return result

    return render_template('index.html', title=category, **result)

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = db.session.scalar(sa.select(Post).where(Post.id == post_id))

    if not post:
        flash("Post not found", "danger")
        return (redirect(url_for('main.index')))
    
    form = PostNewPost(obj=post)

    if form.validate_on_submit():
        post.body = form.body.data
        post.category = form.category.data
        db.session.commit()

        flash("Post Edited")
        return redirect(url_for('main.index'))

    return render_template('edit_post.html', form=form)
    
@bp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    form = Delete()
    if form.validate_on_submit():
        post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', 'info')
        return redirect(url_for('main.index'))
    return render_template('delete_post.html', form=form)

@bp.route('/check_updates')
def check_updates():
    
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None, type=str)
    filter_data = request.args.get('filter')
    posts_with_comment_status = Post.get_posts_with_comment_status(page, filter_data, current_app.config['CATEGORIES'][category])
    
    # Convert the result to a list of dictionaries
    print(posts_with_comment_status)
    
    return posts_with_comment_status