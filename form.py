from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,PasswordField, IntegerField, FloatField, TextAreaField

class SearchForm(FlaskForm):
    mediaName = StringField('Name')
    minyear = StringField('min year')
    maxyear = StringField('max year')
    rating = StringField('rating')
    runtime = StringField('runtime')
    submit = SubmitField('Search')