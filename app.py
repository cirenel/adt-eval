from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from form import SearchForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekrit'
Bootstrap(app)

@app.route("/")
def index():
    time = datetime.now()
    form = SearchForm()
    return render_template('index.html', time=time.strftime("%H:%M -- %d/%m/%y"), form=form)

#from werkzeug.middleware.proxy_fix import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

