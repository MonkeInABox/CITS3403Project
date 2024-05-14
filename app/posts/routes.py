from flask import render_template, flash, redirect, url_for, request
from app.posts.forms import PostNewPost
from app.main.forms import SearchForm, Delete, FilterForm
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

    categories = {
        "Films": "film",
        "Music": "musc",
        "Books": "book"
    }

    if category == None:
        return url_for('main.index')
    elif category not in categories:
        return url_for('main.index')
    
    comment_form = PostNewComment()
    filter_form = FilterForm()

    if comment_form.validate_on_submit() and current_user.is_authenticated:
        # Create a new comment and associate it with the correct post
        post_id = request.form.get('post_id')
        print(f"post id: {post_id}")

        post = Post.query.get(post_id)
        if post:
            new_comment = Comment(body=comment_form.body.data, post_id=post_id, author_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
    posts = Post.get_posts_by_cat(categories[category])

    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)
    else:
        next_url = None

    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)
    else:
        prev_url = None

    return render_template('index.html', title=category, posts=posts.items, next_url=next_url, prev_url=prev_url, comment_form=comment_form, FilterForm = filter_form)

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