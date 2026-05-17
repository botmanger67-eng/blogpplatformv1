from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Post, User
from app.forms import PostForm, CommentForm
from typing import Union

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/')
def index() -> str:
    """List all published posts ordered by publication date."""
    try:
        posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all()
        return render_template('index.html', posts=posts)
    except Exception as e:
        current_app.logger.error(f"Error loading index: {e}")
        flash('An error occurred while loading posts.', 'danger')
        return render_template('index.html', posts=[])


@posts_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post() -> Union[str, redirect]:
    """Create a new blog post."""
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                published=form.published.data,
                author_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('posts.view_post', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating post: {e}")
            flash('An error occurred while creating the post.', 'danger')
    return render_template('create_post.html', form=form)


@posts_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id: int) -> Union[str, redirect]:
    """View a single post and its comments."""
    try:
        post = Post.query.get_or_404(post_id)
        if not post.published and (not current_user.is_authenticated or current_user.id != post.author_id):
            abort(403)
        # ... rest of the function (assuming it continues correctly)
        return render_template('view_post.html', post=post)
    except Exception as e:
        current_app.logger.error(f"Error viewing post {post_id}: {e}")
        flash('An error occurred while viewing the post.', 'danger')
        return redirect(url_for('posts.index'))