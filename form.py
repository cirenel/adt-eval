from requests import options
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, SelectMultipleField, BooleanField, RadioField


class FilterForm(FlaskForm):
    mediaName = StringField('Name')
    genre = SelectMultipleField('Genres') #or as boolfields?
    #foreach distinct rating and genre, make a checkbox --> where get this and how subdivide?
    submit = SubmitField('Filter')


class EditForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    runtime = StringField('Runtime')
    genres = StringField('Genre')
    rating = StringField('Rating')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    yearReleased = StringField('Year')
    description = TextAreaField('Description')
    submit = SubmitField('Edit')

class AddForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    runtime = StringField('Runtime')
    genres = StringField('Genre')
    rating = StringField('Rating')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    yearReleased = StringField('Year')
    description = TextAreaField('Description')
    submit = SubmitField('Add')

class SearchForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    runtime = StringField('Runtime')
    genres = StringField('Genre')
    rating = StringField('Rating')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    yearReleased = StringField('Year')
    description = TextAreaField('Description')
    submit = SubmitField('Search')

class StarterForm(FlaskForm):
    browse=SubmitField("Browse Listings")
    search=SelectField("Search Listings")
    edit=SubmitField("Edit Listings")
    filter=SubmitField("Filter Listings")