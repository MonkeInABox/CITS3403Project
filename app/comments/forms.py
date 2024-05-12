from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length

class PostNewComment(FlaskForm):
    body = TextAreaField('Post Comment', validators=[Length(min=1, max=200)])
    submit = SubmitField('Submit Comment')