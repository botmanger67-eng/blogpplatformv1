import pytest
from app import create_app, db
from app.models import User, Post
from app.forms import PostForm
from flask import url_for

@pytest.fixture(scope='module')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    """Create a test user and a sample post."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='Test content', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        yield user, post
        db.session.query(Post).delete()
        db.session.query(User).delete()
        db.session.commit()

@pytest.fixture
def logged_in_client(client, init_database):
    """Log the test client in as testuser."""
    user, _ = init_database
    with client:
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=True)
        assert response.status_code == 200
        yield client

class TestPostCRUD:
    """Tests for post create, read, update, delete operations."""

    def test_create_post(self, logged_in_client, init_database):
        """Test creating a new post while logged in."""
        response = logged_in_client.post('/post/new', data={
            'title': 'New Post',
            'content': 'New content',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'New Post' in response.data