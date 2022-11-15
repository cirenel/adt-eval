FROM baseImage
RUN apt-get install -qy python3-psycopg2
RUN pip install gunicorn
RUN pip install uvicorn
RUN pip install werkzeug
RUN pip install "cloud-sql-python-connector[pg8000]"
RUN pip install psycopg2-binary 
RUN pip install Flask 
RUN pip install flask-sqlalchemy 
RUN pip install Flask-WTF 
RUN pip install Flask-bootstrap 