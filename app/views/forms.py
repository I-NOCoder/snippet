from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Snippet


class SnippetForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
