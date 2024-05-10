from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired

class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class PostNewComment(FlaskForm):
    body = TextAreaField('Post Comment', validators=[Length(min=1, max=200)])
    submit = SubmitField('Submit Comment')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit Search")

class Delete(FlaskForm):
    submit = SubmitField("Delete")