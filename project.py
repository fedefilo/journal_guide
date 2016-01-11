# 1 check login status with decorator
# 2 delete on cascade al borrar discipline?
# 3 chequear auth status en new disc/new journal
# 4 endpoints en readme y requirements.txt
# 6 delete local picture file 
# 7 redirect to homepage if not logged, to error if not authorized

# Udacity Full Stack Web Developer Nanodegree
# Project 3 - Item catalog
# Journal Catalog App
# by Federico Vasen
# Dec 23, 2015


import os
import random
import string
from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug import secure_filename
from database_setup import Users, Disciplines, Journals, Base
from xmlconverter import *
from flask.ext.seasurf import SeaSurf
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Configuration for uploads
# Files allowed must be smaller than 5 MB and have an extension for images
UPLOAD_FOLDER = 'static/pictures'
ALLOWED_EXTENSIONS = set(
    ['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

# Database settings
engine = create_engine('sqlite:///journals.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Starts app, configs uploads and CSRF protection
# CSRF protection implemented using SeaSurf Flask Module -
# https://github.com/maxcountryman/flask-seasurf
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
csrf = SeaSurf(app)


# Allowed file extensions
def allowed_file(filename):
    ''' Checks whether a file extension is whitelisted'''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Route for rendering Home Page
@app.route('/')
def HomePage():
    allr = session.query(Journals).join(
        Disciplines, Disciplines.id == Journals.discipline_id)
    disciplines = session.query(Disciplines).all()
    return render_template('home.html', title="Home Page", items=allr, disciplines=disciplines)


# Page for each discipline
@app.route('/disciplines/<int:discipline_id>/')
def discipline(discipline_id):
    journals = session.query(Journals).filter_by(discipline_id=discipline_id)
    discipline = session.query(Disciplines).filter_by(id=discipline_id).one()
    return render_template("categories.html", title=discipline.name, discipline=discipline, items=journals)


# Page for each journal
@app.route('/journal/<int:journal_id>/')
def journalPage(journal_id):
    journal = session.query(Journals).filter_by(id=journal_id).one()
    # When no information about picture is in the DB, a default image is displayed
    if journal.picture is None:
        journal.picture = "default.jpg"
    discipline_name = session.query(Disciplines).filter_by(
        id=journal.discipline_id).one()
    return render_template('journal_page.html', title=journal.title, item=journal, discipline=discipline_name.name)


# Add new discipline
@app.route('/new_discipline/', methods=['GET', 'POST'])
def newDiscipline():
    if request.method == 'GET':
        return render_template('new_discipline.html', title="New Discipline")
    if request.method == 'POST':
        newDiscipline = Disciplines(name=request.form['name'])
        session.add(newDiscipline)
        session.commit()
        flash('New discipline successfully added')
        return redirect(url_for('HomePage'))


# Add new journal
@app.route('/new_journal/', methods=['GET', 'POST'])
def newJournal():
    if request.method == 'GET':
        discipline_list = session.query(Disciplines).all()
        return render_template('new_journal.html', title="New Journal", disciplines=discipline_list)
    if request.method == 'POST':
        # Creates a Journal object with the information in the form
        newJournal = Journals(title=request.form['name'], issn=request.form['issn'], publisher=request.form['publisher'], chief_editor=request.form['editor'], issues_per_year=request.form[
                              'issues'], foundation_year=request.form['foundation'], discipline_id=request.form['discipline'], description=request.form['description'], user_id=login_session['user_id'])
        session.add(newJournal)
        session.commit()
        # Queries the DB to get the ID of the new journal and uses it as filename for uploading the image
        journals = session.query(Journals).order_by(Journals.id).all()
        newJournal = journals[-1]
        file = request.files['picture']
        if file and allowed_file(file.filename):
            name, file_extension = os.path.splitext(file.filename)
            # Original filename is replaced by the ID of the new journal. Extension remains unmodified.
            filename = secure_filename(str(newJournal.id)) + file_extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newJournal.picture = filename
            flash('New journal successfully added')
        return redirect(url_for('HomePage'))


# Delete discipline
@app.route('/disciplines/<int:discipline_id>/delete', methods=['GET', 'POST'])
def deleteDiscipline(discipline_id):
    if request.method == 'GET':
        discipline_name = session.query(Disciplines).filter(
            Disciplines.id == discipline_id).one().name
        return render_template('delete_discipline.html', title="Delete discipline", discipline=discipline_name)
    if request.method == 'POST':
        discipline = session.query(Disciplines).filter(
            Disciplines.id == discipline_id).one()
        journals = session.query(Journals).filter(
            Journals.discipline_id == discipline.id).all()
        # Checks whether there are journals registered with the discipline the user intends to delete
        if len(journals) == 0:
            session.delete(discipline)
            session.commit()
            flash('Discipline deleted')
            return redirect(url_for('HomePage'))
        else:
            return render_template('error.html', title="Error", reason="You have to delete all the journals in the discipline first")


# Delete journal
@app.route('/journal/<int:journal_id>/delete', methods=['GET', 'POST'])
def deleteJournal(journal_id):
    journal = session.query(Journals).filter(Journals.id == journal_id).one()
    # Renders and error page if user has not created this object and therefore is not authorized to delete it
    if 'user_id' not in login_session or journal.user_id != login_session['user_id']:
        return render_template('error.html', title="Error", reason="You can only edit or delete the journals you've created")
    if request.method == 'GET':
        return render_template('delete_journal.html', title="Delete journal", journal=journal.title)
    if request.method == 'POST':
        session.delete(journal)
        session.commit()
        flash('Journal deleted')
        return redirect(url_for('HomePage'))


# Edit discipline
@app.route('/disciplines/<int:discipline_id>/edit', methods=['GET', 'POST'])
def editDiscipline(discipline_id):
    discipline = session.query(Disciplines).filter(
        Disciplines.id == discipline_id).one()
    if request.method == 'GET':
        return render_template('editDiscipline.html', title="Edit discipline", discipline=discipline.name)
    if request.method == 'POST':
        if request.form['name']:
            discipline.name = request.form['name']
            flash('Discipline name updated')
        return redirect(url_for('HomePage'))


# Edit journal
@app.route('/journal/<int:journal_id>/edit', methods=['GET', 'POST'])
def editJournal(journal_id):
    journal = session.query(Journals).filter(Journals.id == journal_id).one()
    # Renders and error page if user has not created this object and therefore is not authorized to delete it
    if 'user_id' not in login_session or journal.user_id != login_session['user_id']:
        return render_template('error.html', title="Error", reason="You can only edit or delete the journals you've created")
    if request.method == 'GET':
        discipline_list = session.query(Disciplines).all()
        return render_template('editJournal.html', title="Edit journal", journal=journal, disciplines=discipline_list)
    if request.method == 'POST':
        if request.form['name']:
            journal.title = request.form['name']
        if request.form['issn']:
            journal.issn = request.form['issn']
        if request.form['publisher']:
            journal.publisher = request.form['publisher']
        if request.form['editor']:
            journal.chief_editor = request.form['editor']
        if request.form['discipline']:
            journal.discipline_id = request.form['discipline']
        if request.form['issues']:
            journal.issues_per_year = request.form['issues']
        if request.form['foundation']:
            journal.foundation_year = request.form['foundation']
        if request.form['description']:
            journal.description = request.form['description']
        if request.files['picture']:
            file = request.files['picture']
            if file and allowed_file(file.filename):
                # Original filename is replaced by the ID of the journal being modified. Extension remains unchanged.
                name, file_extension = os.path.splitext(file.filename)
                filename = secure_filename(str(journal.id)) + file_extension
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print "filename: " + filename
                journal.picture = filename
        flash('Journal info updated')
        return redirect(url_for('journalPage', journal_id=journal_id))


# JSON API routes
@app.route('/disciplines/JSON')
def disciplinesJSON():
    disciplines = session.query(Disciplines).all()
    return jsonify(Disciplines=[i.serialize for i in disciplines])


@app.route('/disciplines/<int:discipline_id>/JSON')
def journaldisciplineJSON(discipline_id):
    journal_list = session.query(Journals).filter(
        Journals.discipline_id == discipline_id).all()
    return jsonify(Journals=[j.serialize for j in journal_list])


@app.route('/journal/<int:journal_id>/JSON')
def journalJSON(journal_id):
    journal = session.query(Journals).filter(Journals.id == journal_id).one()
    return jsonify(Journals=[journal.serialize])


# XML endpoints
# With help from library https://github.com/delfick/python-dict2xml
@app.route('/disciplines/XML')
def disciplinesXML():
    disciplines = session.query(Disciplines).all()
    serialized_list = [i.serialize for i in disciplines]
    # Creates a dictionary that properly renders entries in XML according to the documentation of dict2xml
    dictionary = {}
    dictionary['discipline'] = serialized_list
    parsed_xml = dict2xml(dictionary, wrap="discipline", indent="    ")
    return render_template('xml.xml', parsed_xml=parsed_xml)


@app.route('/disciplines/<int:discipline_id>/XML')
def journaldisciplineXML(discipline_id):
    journal_list = session.query(Journals).filter(
        Journals.discipline_id == discipline_id).all()
    serialized_list = [j.serialize for j in journal_list]
    # Creates a dictionary that properly renders entries in XML according to the documentation of dict2xml
    dictionary = {}
    dictionary['journal'] = serialized_list
    parsed_xml = dict2xml(dictionary, wrap="discipline", indent="    ")
    return render_template('xml.xml', parsed_xml=parsed_xml)


@app.route('/journal/<int:journal_id>/XML')
def journalXML(journal_id):
    journal = session.query(Journals).filter(Journals.id == journal_id).one()
    parsed_xml = dict2xml(journal.serialize, wrap="journal", indent="    ")
    return render_template('xml.xml', parsed_xml=parsed_xml)


# User Helper Functions refactored from Udacity's Authorization Course
# https://github.com/udacity/ud330/tree/master

def createUser(login_session):
    '''
    Creates a new user in the DB based on the information in the session cookie.
    Returns the new user's id in the database.

    '''
    newUser = Users(name=login_session['username'], email=login_session[
        'email'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''
    Gets the user object corresponding with an user_id.
    Arg: user_id (integer)
    Returns the user object.

    '''
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''
    Returns an user's id based on his/her email address
    Arg: email (string)
    Returns the user's id (integer).
    If no user registered with that address, returns None.
    '''
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


# Start code for login and logout with Facebook
# Taken from https://github.com/udacity/ud330/tree/master
@csrf.exempt
@app.route('/login')
# Create anti-forgery state token
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# fb connect and disconnect taken from Udacity's authorization course

@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s" % url
    print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in our
    # token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    flash("Now logged in as %s" % login_session['username'])
    return output

@csrf.exempt
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    print result
    login_session.clear()
    return redirect(url_for('HomePage'))

# Run app
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
