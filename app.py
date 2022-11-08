from platform import release
from wsgiref.util import request_uri
from requests import session
import requests
import sqlalchemy
from sqlalchemy import create_engine, insert, update, select, delete 
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from form import AddForm, EditForm, SearchForm, FilterForm, StarterForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from google.cloud.sql.connector import Connector, IPTypes



app = Flask(__name__)
#################
# configuration #
#################

#wow. so secure. much secret.
app.config['SECRET_KEY'] = "sekrit"

clickCnt = 0

#instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
#app.config["SQLALCHEMY_DATABASE_URI"]= f"postgresql+pg8000://{USERNAME}:{PASSWORD}@/{DBNAME}?unix_sock={db_socket_dir}/{PUBLIC_IP_ADDRESS}/.s.PGSQL.5432"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db_user =   "postgres"
db_pass = "Windows2000"
db_name = "nflix"
project = "adt-eval:us-east1:adt-eval-nflix"  # e.g. '/cloudsql/project:region:instance'
sql = "adt-eval-nflix"

'''
#this guy for local connect
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@localhost:5432/{db_name}" #there has to be a way to put this guy in google cloud :think:
'''
#this guy for web deploy
GOOGLE_APPLICATION_CREDENTIALS= '/cred.json' #this is real gross.
def getconn():
    with Connector() as connector:
        conn = connector.connect(
            project, # Cloud SQL Instance Connection Name
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )
        return conn

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}


Bootstrap(app)
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
orderBy = None

###############
# app routing #
###############

@app.route("/",methods=['GET'])
def index():
    time = datetime.now()
    #form options puller
    options = Entries.query.with_entities(Entries.rating).distinct()
    form = StarterForm()
    ratingOptions = Entries.query.with_entities(Entries.rating).distinct()
    countryOptions = Entries.query.with_entities(Entries.country).distinct()
    mediaTypeOptions = Entries.query.with_entities(Entries.media_type).distinct()
    form.search.choices = mediaTypeOptions
    global tab
    global orderBy
    orderBy= Entries.show_id
    tab = Entries.query.order_by(orderBy).paginate(page=1, per_page=10)
    return render_template('index.html', time=time.strftime("%H:%M -- %d/%m/%y"), form=form)

@app.route("/show<int:page>",methods=['GET'])
def showPage(page=1):
    global orderBy
    entryPer = 10
    #tab = db.session.execute(db.select(Entries).order_by(Entries.show_id)).paginate(page,entryPer)
    tab = Entries.query.order_by(orderBy).paginate(page=page, per_page=10)

    return render_template('show.html', table=tab)

@app.route("/search",methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print("boop")
        print(request.headers)
        sqlQuery = "SELECT * FROM entries WHERE "
        titleArg = (lambda:"entries.title LIKE '%'", lambda:"entries.title LIKE \'%"+request.form['mediaName']+"%\'")[request.form['mediaName']!=""]()
        typeArg = (lambda:"entries.media_type LIKE '%'", lambda:"entries.media_type LIKE \'%"+request.form['mediaType']+"%\'")[request.form['mediaType']!=""]()
        rateArg = (lambda:"entries.rating LIKE '%'", lambda:"entries.rating LIKE \'%"+request.form['rating']+"%\'")[request.form['rating']!=""]()
        castArg = (lambda:"entries.cast_list LIKE '%'", lambda:"entries.cast_list LIKE \'%"+request.form['castList']+"%\'")[request.form['castList']!=""]()
        dirArg = (lambda:"entries.director LIKE '%'", lambda:"entries.director LIKE \'%"+request.form['director']+"%\'")[request.form['director']!=""]()
        countArg = (lambda:"entries.country LIKE '%'", lambda:"entries.country LIKE \'%"+request.form['country']+"%\'")[request.form['country']!=""]()
        #print(">> "+countArg)
        relYArg = (lambda:"entries.release_year LIKE '%'", lambda:"entries.release_year LIKE \'%"+request.form['yearReleased']+"%\'")[request.form['yearReleased']!=""]() #coming back a number. comp diff
        durArg = (lambda:"entries.duration LIKE '%'", lambda:"entries.duration LIKE \'%"+request.form['runtime']+"%\'")[request.form['runtime']!=""]()

      #  Arg = (lambda:"", lambda:"entries. LIKE \'%"+request.form['']+"%\'")[request.form['']!=""]()
      #  Arg = (lambda:"", lambda:"entries. LIKE \'%"+request.form['']+"%\'")[request.form['']!=""]()
        sqlQuery = sqlQuery+ titleArg+" AND "+typeArg+" AND "+rateArg+" AND "+castArg+" AND "+dirArg+" AND "+durArg+" AND "+countArg
#        sqlQuery = "SELECT * FROM entries WHERE title LIKE \'%test%\'"
        print(">> "+sqlQuery)
        global tab
        tab = db.session.execute(sqlQuery).all()
        #print(len(tab))
        return render_template('showSearch.html', table=tab, count=len(tab))
    else:
        form=SearchForm()
        return render_template('search.html', form=form)

@app.route("/add",methods=['GET', 'POST'])
def addEntry():
    if request.method=='POST':
        data={'show_id':"s"+str((db.session.query(Entries).count())+2),'title':request.form['mediaName'], 'media_type':request.form['mediaType'], 'director':request.form['director'], 'cast_list':request.form['castList'], 'country':request.form['country'], 'release_year':int(request.form['yearReleased']), 'rating':request.form['rating'], 'duration':request.form['runtime'], 'date_added':datetime.now().date(), 'genre':request.form['genres']}
        cols = ', '.join(f'"{k}"' for k in data.keys())
        vals = ', '.join(f':{k}' for k in data.keys())
       # sqlUpdate = f"""INSERT INTO "entries" ({cols}) VALUES ({vals})"""
       # print(sqlUpdate)
       # db.session.execute(sqlUpdate, data)
        stmt = insert(Entries).values(data)
        db.session.execute(stmt)
        db.session.commit()
        with app.app_context():
            db.create_all()
        msg = "added record"
        return render_template('index.html', time=msg)
    form=AddForm()
    return render_template('editEntry.html', form=form)

@app.route("/delete<string:show_id>", methods=['GET','POST'])
def deleteEntry(show_id):
    print(show_id)
    entryPer = 10
    stmt = delete(Entries).where(Entries.show_id == show_id)
    db.session.execute(stmt)
    db.session.commit()
    with app.app_context():
        db.create_all()
    print(stmt)
    tab = Entries.query.order_by(Entries.show_id).paginate(page=1, per_page=entryPer)
    return render_template('show.html', table=tab)

@app.route("/edit<string:show_id>",methods=['GET', 'POST'])
def editEntry(show_id="s1", msg=""):
    if request.method=='POST':
        sqlUpdate = "UPDATE entries SET title= \'"+request.form['mediaName']+"\', media_type= \'"+request.form['mediaType']+"\', director= \'"+request.form['director']+"\', cast_list= \'"+request.form['castList']+"\',  country= \'"+request.form['country']+"\',   release_year= \'"+request.form['yearReleased']+"\',  rating= \'"+request.form['rating']+"\',  duration= \'"+request.form['runtime']+"\'  WHERE show_id=\'"+show_id+"\'"
        print(sqlUpdate)
        db.session.execute(sqlUpdate)
        db.session.commit()
        with app.app_context():
            db.create_all()
        msg = "updated record"
    form = EditForm()
    result = Entries.query.filter(Entries.show_id == show_id).all()
    print(show_id)
    print(len(result))
    form.mediaName.data = result[0].title
    form.mediaType.data = result[0].media_type
    form.description.data = result[0].description
    form.genres.data = result[0].genre
    form.director.data = result[0].director
    form.castList.data = result[0].cast_list
    form.country.data = result[0].country
    form.rating.data = result[0].rating
    form.runtime.data = result[0].duration
    form.yearReleased.data = result[0].release_year
    return render_template('editEntry.html', form=form, result=result, msg=msg)

@app.route("/sortBy<string:sort><int:page>", methods=['GET'])
def sortBy(sort, page):
    #this is kinda gross. there *has* to be a better way
    global orderBy
   # tab = Entries.query.order_by(Entries.show_id).paginate(page=page, per_page=10)
    global clickCnt
    core = None
    #ugh. update to 3.10 for match-case :-T
    if( sort == "title"):
        core = Entries.title
    elif( sort == "type"):
        core=Entries.media_type
    elif( sort == "duration"):
        core = Entries.duration
    elif( sort == "description"):
        core = Entries.description
    elif( sort == "date_add"):
        core = Entries.date_added
    elif(sort == "country"):
        core = Entries.country
    elif(sort == "genre"):
        core = Entries.genre
    elif(sort == "director"):
        core=Entries.director
    elif(sort == "cast"):
        core=Entries.cast_list
    if( clickCnt % 2 == 1):
        core = core.desc()
    orderBy = core
    tab = Entries.query.order_by(core).paginate(page=page, per_page=10)
    clickCnt = clickCnt+1
    return render_template('show.html', table=tab)

def demoSel():
    result  = db.session.execute(db.select(Entries).order_by(Entries.show_id)).scalars()
    return result

########################
# sqlalchemy db models #
########################
class Entries(db.Model):
    show_id = db.Column(db.String, primary_key=True)
    media_type = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    director = db.Column(db.String)
    cast_list=db.Column(db.String)
    country=db.Column(db.String)
    rating=db.Column(db.String)
    duration=db.Column(db.String)
    genre = db.Column(db.String)
    date_added  = db.Column(db.DateTime)
    release_year = db.Column(db.Integer)

class Countries(db.Model):
    country_id = db.Column(db.String, primary_key=True)
    country = db.Column(db.String)

class Genres(db.Model):
    genre_id = db.Column(db.String, primary_key = True)
    genre = db.Column(db.String)


#from werkzeug.middleware.proxy_fix import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

