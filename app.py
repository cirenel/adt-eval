from platform import release
import sqlalchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from form import AddForm, EditForm, SearchForm, FilterForm, StarterForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
###############
# configuration
###############

#wow. so secure. much secret.
app.config['SECRET_KEY'] = "sekrit"
USERNAME = "postgres"
PASSWORD = "Windows2000"
DBNAME = "nflix"
PUBLIC_IP_ADDRESS ="34.138.118.222"
PROJECT_ID ="adt-eval"
INSTANCE_NAME ="adt-eval-nflix"
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

#app.config["SQLALCHEMY_DATABASE_URI"]= f"postgresql+pg8000://{USERNAME}:{PASSWORD}@/{DBNAME}?unix_sock={db_socket_dir}/{PUBLIC_IP_ADDRESS}/.s.PGSQL.5432"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

#app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{DBNAME}" #there has to be a way to put this guy in google cloud :think:
db_user =   "postgres"
db_pass = "Windows2000"
db_name = "nflix"
unix_socket_path = "/cloudsql/adt-eval:us-east1:adt-eval-nflix"  # e.g. '/cloudsql/project:region:instance'

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
    #                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
    # Note: Some drivers require the `unix_sock` query parameter to use a different key.
    # For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
    sqlalchemy.engine.url.URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_sock": "{}/.s.PGSQL.5432".format(unix_socket_path)},
    ),
    pool_size = 5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle = 1800
)
app.config["SQLALCHEMY_DATABASE_URI"] = pool.url
Bootstrap(app)
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


############
#app routing
############

@app.route("/",methods=['GET'])
def index():
    time = datetime.now()
    #form options puller
    options = Entries.query.with_entities(Entries.rating).distinct()
    print(options)
    print(options[0], options[1], options[-1])
    form = StarterForm()
    return render_template('index.html', time=time.strftime("%H:%M -- %d/%m/%y"), form=form)

@app.route("/show<int:page>",methods=['GET'])
def showPage(page=1):
    entryPer = 10
    #tab = db.session.execute(db.select(Entries).order_by(Entries.show_id)).paginate(page,entryPer)
    tab = Entries.query.order_by(Entries.show_id).paginate(page=page, per_page=entryPer)
    return render_template('show.html', table=tab)

@app.route("/search",methods=['GET', 'POST'])
def search():
    form=SearchForm()
    return render_template('search.html', form=form)

@app.route("/add",methods=['GET', 'POST'])
def addEntry():
    form=AddForm()
    return render_template('editEntry.html', form=form)

@app.route("/edit<string:show_id>",methods=['GET', 'POST'])
def editEntry(show_id="s1"):
    form = EditForm()
    result = Entries.query.filter(Entries.show_id == show_id).all()
    print(show_id)
    print(len(result))
    form.mediaName.data = result[0].title
    form.mediaType.data = result[0].media_type
    form.description.data = result[0].description
    form.genres.data = result[0].genre
    form.director.data = result[0].director
    form.cast.data = result[0].cast_list
    form.rating.data = result[0].rating
    form.runtime.data = result[0].duration
    form.yearReleased.data = result[0].release_year
    return render_template('editEntry.html', form=form, result=result)


def demoSel():
    result  = db.session.execute(db.select(Entries).order_by(Entries.show_id)).scalars()
    return result

###########################
#sqlalchemy supportive bits
###########################
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

###########################
# https://cloud.google.com/sql/docs/postgres/connect-app-engine-standard
# friend documentation for connecting to cloud postgresql instance 
###########################
# connect_unix_socket initializes a Unix socket connection pool for
# a Cloud SQL instance of Postgres.


#from werkzeug.middleware.proxy_fix import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

