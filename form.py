from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, SelectMultipleField, BooleanField, RadioField


class SearchForm(FlaskForm):
    mediaName = StringField('Name')
    minyear = StringField('min year')
    maxyear = StringField('max year')
    rating = StringField('rating')
    runtime = StringField('runtime')
    submit = SubmitField('Search')

class FilterForm(FlaskForm):
    mediaName = StringField('Name')
    genre = SelectMultipleField('Genres') #or as boolfields?
    #foreach distinct rating and genre, make a checkbox --> where get this and how subdivide?
    submit = SubmitField('Filter')

class AddForm(FlaskForm):
    mediaName = StringField('Name')
    submit = SubmitField('Add')

class EditForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    runtime = StringField('Runtime')
    description = StringField('Description')
    genres = StringField('Genre')
    rating = StringField('Rating')
    director = StringField('Director')
    cast = StringField('Cast')
    yearReleased = StringField('Year')
    submit = SubmitField('Edit')

class AddForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    runtime = StringField('Runtime')
    description = StringField('Description')
    genres = StringField('Genre')
    rating = StringField('Rating')
    director = StringField('Director')
    cast = StringField('Cast')
    yearReleased = StringField('Year')
    submit = SubmitField('Add')
    
class SearchForm(FlaskForm):
    mediaName = StringField('Name')
    mediaType = StringField('Type')
    runtime = StringField('Runtime')
    description = StringField('Description')
    genres = StringField('Genre')
    rating = StringField('Rating')
    director = StringField('Director')
    cast = StringField('Cast')
    yearReleased = StringField('Year')
    submit = SubmitField('Search')

class StarterForm(FlaskForm):
    browse=SubmitField("Browse Listings")
    search=SubmitField("Search Listings")
    edit=SubmitField("Edit Listings")
    filter=SubmitField("Filter Listings")