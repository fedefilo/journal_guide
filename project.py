import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Users, Disciplines, Journals, Base
#from oauth import *
from werkzeug import secure_filename


UPLOAD_FOLDER = 'static/pictures'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


engine = create_engine('sqlite:///journals.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Home Page
@app.route('/')
def HomePage():
	allr = session.query(Journals).all()
	disciplines = session.query(Disciplines).all()
	return render_template('home.html', title = "HomePage", items = allr, disciplines = disciplines)

# Page for each discipline
@app.route('/disciplines/<int:discipline_id>/')
def discipline(discipline_id):
	journals = session.query(Journals).filter_by(discipline_id = discipline_id)
	discipline_name = session.query(Disciplines).filter_by(id = discipline_id).one()
	return render_template("categories.html", title = discipline_name.name, items = journals, name = discipline_name.name)

# Page for each journal
@app.route('/journal/<int:journal_id>/')
def journalPage(journal_id):
	journal = session.query(Journals).filter_by(id = journal_id).one()
	if journal.picture is None:
		journal.picture = "default.jpg"
	discipline_name = session.query(Disciplines).filter_by(id = journal.discipline_id).one()
	return render_template('journal_page.html', title = journal.title, item = journal, discipline = discipline_name.name)

# Add new discipline
@app.route('/new_discipline/', methods=['GET','POST'])
def newDiscipline():
	if request.method == 'GET':
		return render_template('new_discipline.html', title = "New Discipline")
	if request.method == 'POST':
		newDiscipline = Disciplines(name= request.form['name'])
		session.add(newDiscipline)
		session.commit()
		flash('New discipline successfully added')
		return redirect(url_for('HomePage'))


# Add new journal
@app.route('/new_journal/', methods=['GET','POST'])
def newJournal():
	if request.method == 'GET':
		discipline_list = session.query(Disciplines).all()
		return render_template('new_journal.html', title = "New Journal", disciplines = discipline_list)
	if request.method == 'POST':
		newJournal = Journals(title= request.form['name'], issn = request.form['issn'], publisher = request.form['publisher'], chief_editor = request.form['editor'], issues_per_year = request.form['issues'], foundation_year = request.form['foundation'], discipline_id = request.form['discipline'],description = request.form['description'])
		session.add(newJournal)
		session.commit()
		journals = session.query(Journals).order_by(Journals.id).all()
		newJournal = journals[-1]
		file = request.files['picture']
		if file and allowed_file(file.filename):
			name, file_extension = os.path.splitext(file.filename)
			filename = secure_filename(str(newJournal.id)) + file_extension
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			newJournal.picture = filename
		return redirect(url_for('HomePage'))

# Delete discipline

@app.route('/disciplines/<int:discipline_id>/delete', methods = ['GET', 'POST'])
def deleteDiscipline(discipline_id):
	if request.method == 'GET':
		discipline_name = session.query(Disciplines).filter(Disciplines.id == discipline_id).one().name
		return render_template('delete_discipline.html', title = "Delete discipline", discipline = discipline_name)
	if request.method == 'POST':
			discipline = session.query(Disciplines).filter(Disciplines.id == discipline_id).one()
			journals = session.query(Journals).filter(Journals.discipline_id == discipline.id).all()
			if len(journals) == 0:
				session.delete(discipline)
				session.commit()
				return redirect(url_for('HomePage'))
			else:
				return render_template('disciplineNotEmpty.html')

# Delete journal

@app.route('/journal/<int:journal_id>/delete', methods = ['GET', 'POST'])
def deleteJournal(journal_id):
	journal = session.query(Journals).filter(Journals.id == journal_id).one()
	if request.method == 'GET':
		return render_template('delete_journal.html', title = "Delete journal", journal = journal.title)
	if request.method == 'POST':
		session.delete(journal)
		session.commit()
		return redirect(url_for('HomePage'))
			




# @app.route('/login')

# # Create anti-forgery state token
# def showLogin():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in xrange(32))
#     login_session['state'] = state
#     return render_template('login.html', STATE=state)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)

