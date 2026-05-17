import pytest
from flask import url_for
from app import create_app, db
from app.models import User


@pytest.fixture(scope='module')
def test_app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='module')
def client(test_app):
    """A test client for the application."""
    return test_app.test_client()


@pytest.fixture(scope='module')
def runner(test_app):
    """A test CLI runner for the application."""
    return test_app.test_cli_runner()


def register_user(client, username: str, email: str, password: str, confirm_password: str) -> 'flask.Response':
    """Helper function to register a user."""
    return client.post(url_for('auth.register'), data=dict(
        username=username,
        email=email,
        password=password,
        confirm_password=confirm_password
    ), follow_redirects=True)


def login_user(client, username: str, password: str) -> 'flask.Response':
    """Helper function to log in a user."""
    return client.post(url_for('auth.login'), data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout_user(client) -> 'flask.Response':
    """Helper function to log out the current user."""
    return client.get(url_for('auth.logout'), follow_redirects=True)


def test_register_page_loads(client) -> None:
    """Test that the registration page loads successfully."""
    response = client.get(url_for('auth.register'))
    assert response.status_code == 200
    assert b'Register' in response.data


def test_login_page_loads(client) -> None:
    """Test that the login page loads successfully."""
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200