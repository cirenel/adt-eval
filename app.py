from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from form import SearchForm, FilterForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

#wow. so secure. much secret.
app.config['SECRET_KEY'] = "sekrit"
username = "postgres"
password = "Windows2000"
dbname = "nflix"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{dbname}" #there has to be a way to put this guy in google cloud :think:

Bootstrap(app)
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

#app routing
@app.route("/")
def index():
    time = datetime.now()
    form = SearchForm() 
    tab = demoSel()
    return render_template('index.html', time=time.strftime("%H:%M -- %d/%m/%y"), form=form, table=tab)


#sql supportive bits
def demoSel():
    result  = db.session.execute(db.select(Entries).order_by(Entries.show_id)).scalars()
    return result; 

#sqlalchemy supportive bits
class Entries(db.Model):
    show_id = db.Column(db.String, primary_key=True)


#from werkzeug.middleware.proxy_fix import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

