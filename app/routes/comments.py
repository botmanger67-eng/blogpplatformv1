from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post, Comment
from app.forms import CommentForm

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/post/<int:post_id>/comment/new', methods=['GET', 'POST'])
@login_required
def create_comment(post_id: int):
    """Create a new comment on a post."""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        try:
            comment = Comment(
                content=form.content.data,
                author=current_user,
                post=post
            )
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added.', 'success')
            return redirect(url_for('posts.view_post', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while posting your comment. Please try again.', 'danger')
            # Log the error in production
    return render_template('create_comment.html', form=form, post=post)

@comments_bp.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id: int):
    """Edit an existing comment (only by its author)."""
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm(obj=comment)
    if form.validate_on_submit():
        try:
            comment.content = form.content.data
            db.session.commit()
            flash('Comment updated.', 'success')
            return redirect(url_for('posts.view_post', post_id=comment.post.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update comment. Please try again.', 'danger')
    return render_template('edit_comment.html', form=form, comment=comment)