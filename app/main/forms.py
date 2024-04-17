from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length

class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class PostNewPost(FlaskForm):
    body = TextAreaField('Post Body', validators=[Length(min=0, max=200)])
    submit = SubmitField('Submit Post')