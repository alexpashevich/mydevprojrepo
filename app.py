# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask import send_from_directory, g, redirect
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__, static_url_path='')
DATABASE = 'db.sqlite3'
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'studyabroaddreamsender@gmail.com',
    MAIL_PASSWORD = 'Topol123',
))
mail = Mail(app)

# DB stuff start
def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# DB stuff end

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grants/<int:page_nb>')
def grants(page_nb):
    grants = query_db('select * from grants')
    return render_template('grants.html', grants=grants)

@app.route('/grants-detailed/<int:grant_id>')
def show_user_profile(grant_id):
    grants = query_db('select * from grants where grant_id = %d' % grant_id)
    return render_template('grant_detail.html', grant=grants[0])

@app.route('/prices/')
def prices():
    return render_template('prices.html')

@app.route('/references/')
def references():
    return render_template('references.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/grants-img/<path:path>')
def send_grant_img(path):
    return send_from_directory('grants-img', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/send-form/', methods=['POST'])
def send_email():
    full_message = request.form['social'] + u"\nСообщение: " + request.form['message']
    msg = Message(subject="[StudyAbroadDream] Message from " + request.form['name'],
                  body=full_message,
                  sender=request.form['email'],
                  recipients=["psbl94@gmail.com"])
    mail.send(msg)
    return render_template('contact-form-thank-you.html')

if __name__ == '__main__':
    app.debug = True
    app.run()