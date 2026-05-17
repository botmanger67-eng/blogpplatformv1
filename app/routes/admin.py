from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import exc
from typing import List, Optional

from app import db
from app.models import User, Post, Comment
from app.routes.auth import admin_required

# Minimal CSRF-protected form for admin actions
class EmptyForm(FlaskForm):
    """Form used solely for CSRF validation on action POSTs."""
    pass

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard() -> str:
    """Render the admin dashboard with counts and recent activity."""
    try:
        user_count: int = User.query.count()
        post_count: int = Post.query.count()
        comment_count: int = Comment.query.count()
        # Recent posts (last 10)
        recent_posts: List[Post] = Post.query.order_by(Post.created_at.desc()).limit(10).all()
        # Recent comments (last 10)
        recent_comments: List[Comment] = Comment.query.order_by(Comment.created_at.desc()).limit(10).all()
        # Recent registrations (last 10 users)
        recent_users: List[User] = User.query.order_by(User.created_at.desc()).limit(10).all()
    except exc.SQLAlchemyError:
        flash('Database error occurred. Please try again later.', 'danger')
        return redirect(url_for('main.index'))  # assuming a main index or home

    return render_template(
        'admin.html',
        user_count=user_count,
        post_count=post_count,
        comment_count=comment_count,
        recent_posts=recent_posts,
        recent_comments=recent_comments,
        recent_users=recent_users,
        empty_form=EmptyForm()
    )

@admin_bp.route('/users')
@login_required
@admin_required
def list_users() -> str:
    """Display all registered users with management actions."""
    try:
        users: List[User] = User.query.order_by(User.created_at.desc()).all()
    except exc.SQLAlchemyError:
        flash('Database error occurred. Please try again later.', 'danger')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin_users.html', users=users, empty_form=EmptyForm())