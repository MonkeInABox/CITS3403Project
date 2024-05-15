from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired

class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit Search")

class Delete(FlaskForm):
    submit = SubmitField("Delete")

class FilterForm(FlaskForm):
    filter = SelectField("Filter Posts: ",
                            choices=[
                               ('nwst', 'Newest'),   # DO NOT GO ABOVE 4 CHARS FOR DATABASE VALUE
                               ('ldst', 'Oldest'),  # DATABASE CAN ONLY HANDLE 4 CHARS!!!
                               ('mslk', 'Most Liked'),
                               ('msdk', 'Most disliked'),
                               ('mscm', 'Most Commented')
                           ],
                           default = 'nwst')
    submit = SubmitField("Submit Filter")