from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import Length

class PostNewPost(FlaskForm):
    body = TextAreaField('Post Body', validators=[Length(min=0, max=200)], id="post")
    category = SelectField('What category is this post?',
                           choices=[
                               ('film', 'Films'),   # DO NOT GO ABOVE 4 CHARS FOR DATABASE VALUE
                               ('musc', 'Music'),  # DATABASE CAN ONLY HANDLE 4 CHARS!!!
                               ('book', 'Books'),
                               ('tvsh', 'TV Shows'),
                               ('vdga', 'Video Games')
                           ],
                           default='film')
    submit = SubmitField('Submit Post')