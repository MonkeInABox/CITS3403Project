from flask import render_template, flash, redirect, url_for
from app.main.forms import Delete
from flask_login import login_required
import sqlalchemy as sa
from app.models import Comment
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