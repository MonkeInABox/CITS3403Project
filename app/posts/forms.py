from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import Length
from flask import current_app

class PostNewPost(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(PostNewPost, self).__init__(*args, **kwargs)
        self.category.choices = [(value, key) for key, value in current_app.config['CATEGORIES'].items()]

    body = TextAreaField('Post Body', validators=[Length(min=0, max=200)], id="post")
    category = SelectField('What category is this post?')
    submit = SubmitField('Submit Post')