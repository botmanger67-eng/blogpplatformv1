from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SubmitField,
    BooleanField,
    SelectField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Optional,
)
from flask_login import current_user
from app.models import User, Category


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username", validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(3, 64, message="Username must be between 3 and 64 characters."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(1, 120),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(6, 128, message="Password must be at least 6 characters."),
        ],
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """Check if username is already taken."""
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("That username is already taken. Please choose a different one.")

    def validate_email(self, email):
        """Check if email is already registered."""
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("That email is already registered.")