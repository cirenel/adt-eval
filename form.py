from requests import options
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, SelectMultipleField, BooleanField, RadioField


class FilterForm(FlaskForm):
    mediaName = StringField('Name')
    genre = SelectMultipleField('Genres') #or as boolfields?
    #foreach distinct rating and genre, make a checkbox --> where get this and how subdivide?
    submit = SubmitField('Filter')

class BaseForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    runtime = StringField('Runtime')
    dateAdded = StringField('Date Added')
    yearReleased = StringField('Year')
    rating = StringField('Rating')
    genres = StringField('Genre')
    description = TextAreaField('Description')
    submit = SubmitField('CHANGETHIS')

class StarterForm(FlaskForm):
    browse=SubmitField("Browse Listings")
    search=SelectField("Search Listings")
    edit=SubmitField("Edit Listings")
    filter=SubmitField("Filter Listings")

class SearchForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    runtime = StringField('Runtime')
    dateAdded = StringField('Date Added')
    yearReleased = StringField('Year')
    rating = StringField('Rating')
    genres = StringField('Genre')
    description = TextAreaField('Description')
    submit = SubmitField('Search')

class AddForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    runtime = StringField('Runtime')
    dateAdded = StringField('Date Added')
    yearReleased = StringField('Year')
    rating = StringField('Rating')
    genres = StringField('Genre')
    description = TextAreaField('Description')
    submit = SubmitField('Add')
    
class EditForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    director = StringField('Director')
    castList = StringField('Cast')
    country = StringField('Country')
    runtime = StringField('Runtime')
    dateAdded = StringField('Date Added')
    yearReleased = StringField('Year')
    rating = StringField('Rating')
    genres = StringField('Genre')
    description = TextAreaField('Description')
    submit = SubmitField('Edit')
    
