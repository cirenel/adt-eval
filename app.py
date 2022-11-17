from email.mime import base
from platform import release
from wsgiref.util import request_uri
from requests import RequestException, session
import requests
import sqlalchemy
from sqlalchemy import create_engine, insert, update, select, delete
from flask_sqlalchemy import SQLAlchemy
import os
from form import  BaseForm, FilterForm, StarterForm
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
from google.cloud.sql.connector import Connector, IPTypes


#######################
# setup/configuration #
#######################

app = Flask(__name__)

#wow. so secure. much secret.
app.config['SECRET_KEY'] = "sekrit"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

clickCnt = 0 #used to count number of times a sorting option has been clicked on

#working with different sqlalchemy configurations for db connection
#instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
#app.config["SQLALCHEMY_DATABASE_URI"]= f"postgresql+pg8000://{USERNAME}:{PASSWORD}@/{DBNAME}?unix_sock={db_socket_dir}/{PUBLIC_IP_ADDRESS}/.s.PGSQL.5432"

#from werkzeug.middleware.proxy_fix import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

db_user = "postgres"
db_pass = "Windows2000"
db_name = "nflix"
project = "adt-eval:us-east1:adt-eval-nflix"  # e.g. '/cloudsql/project:region:instance'
sql = "adt-eval-nflix"

'''
#comment in this line for local db connect
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@localhost:5432/{db_name}" #there has to be a way to put this guy in google cloud :think:
'''
#comment in this block for when web deploying for cloud SQL connection
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
#build db tables
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

#global app-wide vars
orderBy = None #sorting values
filterBy = None #filtering values
lastPull = None #last table from DB query


###############
# app routing #
###############

@app.route("/",methods=['GET'])
def index():
    global lastPull
    global orderBy
    orderBy= Entries.show_id
    lastPull = Entries.query.order_by(orderBy)
    return render_template('index.html')

@app.route("/show/<int:page>",methods=['GET', 'POST'])
def showPage(page=1, tab=None):
    global orderBy
    global lastPull
    entryPer = 10
    #tab = db.session.execute(db.select(Entries).order_by(Entries.show_id)).paginate(page,entryPer)
    if lastPull is None:
        lastPull = Entries.query.order_by(orderBy)
    tab = lastPull
    return render_template('show.html', table=tab.paginate(page=page, per_page=10))


@app.route("/sortBy/<string:sort>/<int:page>", methods=['GET'])
def sortBy(sort, page=1, table=lastPull):
    #this is kinda gross. there *has* to be a better way
    global orderBy
   # tab = Entries.query.order_by(Entries.show_id).paginate(page=page, per_page=10)
    global clickCnt
    global lastPull
    core = None
    #ugh. update to 3.10 for match-case
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
    if table == lastPull:
        lastPull = lastPull.order_by(core)
    elif table is not None:
        lastPull = table.order_by(core)
    else:
        lastPull = Entries.query.order_by(core)
    clickCnt = clickCnt+1
    return render_template('show.html', table=lastPull.paginate(page=page, per_page=10))


@app.route("/filter", methods=['POST'])
def showFilter():
    global lastPull
    if lastPull is None:
        lastPull = Entries.query.order_by(orderBy)
    tab = lastPull

    if len(request.form['title'])> 0:
        tab = tab.filter(Entries.title.contains(request.form['title']))

    if len(request.form['duration'])> 0:
        tab = tab.filter(Entries.duration.contains(request.form['duration']))

    if len(request.form['director'] )> 0:
        tab = tab.filter(Entries.director.contains(request.form['director']))

    if len(request.form['cast'])> 0:
        tab = tab.filter(Entries.cast_list.contains(request.form['cast']))

    if len(request.form.getlist('type')) > 0:
        for t in request.form.getlist('type'):
            tab = tab.filter(Entries.media_type.contains(t))

    if len(request.form.getlist('genre')) > 0:
        for g in request.form.getlist('genre'):
            tab = tab.filter(Entries.genre.contains(g))

    if len(request.form['rating']) > 0:
        tab = tab.filter(Entries.rating.contains(request.form['rating']))

    lastPull = tab.order_by(orderBy)
    return render_template('show.html', table=tab.paginate(page=1, per_page=10))

@app.route("/search",methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sqlQuery = "SELECT * FROM entries WHERE entries.show_id LIKE '%' "
        titleArg = (lambda:"", lambda:"AND entries.title LIKE \'%"+request.form['mediaName']+"%\'")[request.form['mediaName']!=""]()
        typeArg = (lambda:"", lambda:"AND entries.media_type LIKE \'%"+request.form['mediaType']+"%\'")[request.form['mediaType']!=""]()
        rateArg = (lambda:"", lambda:"AND entries.rating LIKE \'%"+request.form['rating']+"%\'")[request.form['rating']!=""]()
        castArg = (lambda:"", lambda:"AND entries.cast_list LIKE \'%"+request.form['castList']+"%\'")[request.form['castList']!=""]()
        dirArg = (lambda:"", lambda:"AND entries.director LIKE \'%"+request.form['director']+"%\'")[request.form['director']!=""]()
        countArg = (lambda:"", lambda:"AND entries.country LIKE \'%"+request.form['country']+"%\'")[request.form['country']!=""]()
        #print(">> "+countArg)
        relYArg = (lambda:"", lambda:"AND entries.release_year LIKE \'%"+request.form['yearReleased']+"%\'")[request.form['yearReleased']!=""]() #coming back a number. comp diff
        durArg = (lambda:"", lambda:"AND entries.duration LIKE \'%"+request.form['runtime']+"%\'")[request.form['runtime']!=""]()

      #  Arg = (lambda:"", lambda:"entries. LIKE \'%"+request.form['']+"%\'")[request.form['']!=""]()
      #  Arg = (lambda:"", lambda:"entries. LIKE \'%"+request.form['']+"%\'")[request.form['']!=""]()
        sqlQuery = sqlQuery+ titleArg+ typeArg +rateArg +castArg +dirArg +durArg +countArg
#        sqlQuery = "SELECT * FROM entries WHERE title LIKE \'%test%\'"
        print(">> "+sqlQuery)
        tab = db.session.execute(sqlQuery).all()
#        print(tab)
        return render_template('showSearch.html', table=tab, count=len(tab))
    else:
        form=BaseForm()
        form['submit'].label.text = "Search"
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
        global lastPull
        lastPull = Entries.query.order_by(orderBy)
        return render_template('index.html', time=msg)
    form=BaseForm()
    form['submit'].label.text = "Add Entry"
    return render_template('editEntry.html', form=form)

@app.route("/delete/<string:show_id>", methods=['GET','POST'])
def deleteEntry(show_id):
    print(show_id)
    entryPer = 10
    stmt = delete(Entries).where(Entries.show_id == show_id)
    db.session.execute(stmt)
    db.session.commit()
    with app.app_context():
        db.create_all()
    print(stmt)
    global lastPull
    lastPull = Entries.query.order_by(orderBy)
    return render_template('show.html', table=lastPull.paginate(page=1, per_page=entryPer))

@app.route("/edit/<string:show_id>",methods=['GET', 'POST'])
def editEntry(show_id="s1", msg=""):
    if request.method=='POST':
        sqlUpdate = "UPDATE entries SET title= \'"+stripApos(request.form['mediaName'])+"\', media_type= \'"+stripApos(request.form['mediaType'])+"\', director= \'"+stripApos(request.form['director'])+"\', cast_list= \'"+stripApos(request.form['castList'])+"\',  country= \'"+request.form['country']+"\',   release_year= \'"+request.form['yearReleased']+"\',  rating= \'"+request.form['rating']+"\',  duration= \'"+request.form['runtime']+"\'  WHERE show_id=\'"+show_id+"\'"
        print(sqlUpdate)
        db.session.execute(sqlUpdate)
        db.session.commit()
        with app.app_context():
            db.create_all()
        msg = "updated record"
        global lastPull
        lastPull = Entries.query.order_by(orderBy)
    result = Entries.query.filter(Entries.show_id == show_id).all()
    form = BaseForm()
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
    form['submit'].label.text = "Edit Entry"
    return render_template('editEntry.html', form=form, result=result, msg=msg)


#just used to pull the information and check for signs of life
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

#additional tables --> thought being to normalize the db
class Countries(db.Model):
    country_id = db.Column(db.String, primary_key=True)
    country = db.Column(db.String)

class Genres(db.Model):
    genre_id = db.Column(db.String, primary_key = True)
    genre = db.Column(db.String)


def stripApos(str):
    return str.replace('\'', '\'\'')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

