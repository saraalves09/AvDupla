from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.widgets import TextArea

from instagram.models import User

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    btn = SubmitField('Login!')


class FormCreateNewAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    checkPassword = PasswordField('Check Password', validators=[DataRequired(), Length(6, 20), EqualTo('password')])
    btn = SubmitField('Create!')

    def validate_email(self, email):
        email_of_user = User.query.filter_by(email=email.data).first()
        if email_of_user:
            return ValidationError('~ this email is already being used ~')

class FormCreateNewPost(FlaskForm):
    text = StringField('What are you thinking today?', widget=TextArea(), validators=[DataRequired()])
    photo = FileField('ADD photo', validators=[DataRequired()])
    btn = SubmitField('Publish')

class CommentForm(FlaskForm):
    comment_text = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')
