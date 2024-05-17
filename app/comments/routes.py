from flask import render_template, flash, redirect, url_for, render_template_string, request, jsonify
from app.main.forms import Delete
from flask_login import login_required, current_user
import sqlalchemy as sa
from app.models import Comment, Post, Like, Dislike
from app.comments import bp
from app.comments.forms import PostNewComment
from app import db

@bp.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    form = Delete()
    if form.validate_on_submit():
        comment = db.first_or_404(sa.select(Comment).where(Comment.id == comment_id))
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted', 'info')
        return redirect(url_for('main.index'))
    return render_template('delete_comment.html', form=form)

@bp.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = db.session.scalar(sa.select(Comment).where(Comment.id == comment_id))  

    if not comment:
        flash("Comment not found.", "danger")
        return redirect(url_for('main.index'))

    form = PostNewComment(obj=comment)  # Pre-fill form with current post data
    
    if form.validate_on_submit():  # Ensure form is valid on submit
        comment.body = form.body.data  # Assign new content
        db.session.commit()  # Commit the changes
        flash("Comment updated successfully.", "success")  # Inform the user
        return redirect(url_for('main.index'))  # Redirect to the main page

    return render_template('edit_comment.html', form=form)  # Render the edit form on GET

# Define a route to fetch comments for a specific post
@bp.route('/get_comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    # Retrieve comments for the specified post (Replace this with your logic)
    post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
    comments = (
    db.session.query(Comment)
    .filter(Comment.post_id == post.id)
    .outerjoin(Like)
    .outerjoin(Dislike)
    .group_by(Comment.id)
    .order_by(sa.desc(sa.func.count(Like.id) - sa.func.count(Dislike.id)))
    .all()
    )   
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