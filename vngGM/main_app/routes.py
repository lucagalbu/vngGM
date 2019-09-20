from main_app import app, db
from main_app.forms import AddUser, AddSchedule
from flask import render_template, flash, redirect, url_for
from main_app.models import Users, Papers, Schedules

@app.route('/')
@app.route('/index')
def index():
	schedules = db.session.query(Users, Schedules).join(Users).order_by('date').all()
	return render_template('index.html', title='Tmp', schedules=schedules)

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/addUser', methods = ['POST', 'GET'])
def addUser():
	form = AddUser()
	
	if form.validate_on_submit():
		user = Users(name=form.name.data, surname=form.surname.data, email=form.email.data)
		db.session.add(user)
		db.session.commit()
		flash('User {} {}, succesfully added'.format(form.name.data, form.surname.data))
		return redirect(url_for('admin'))

	return render_template('addUser.html', form = form)

@app.route('/listUsers')
def listUsers():
	users = Users.query.all()
	return render_template('listUsers.html', users=users)

@app.route('/addSchedule', methods = ['POST', 'GET'])
def addSchedule():
	form = AddSchedule()
	
	if form.validate_on_submit():
		user=Users.query.filter_by(name=form.speaker.data).first()
		schedule = Schedules(speaker_id=user.id, date=form.date.data, extra_info=form.discussion.data)
		db.session.add(schedule)

		user=Users.query.filter_by(name=form.paper_proposer.data).first()
		paper = Papers(title=form.paper_title.data, url=form.paper_url.data, doi=form.paper_doi.data, proposer_id=user.id)
		db.session.add(paper)
		db.session.commit()
		return redirect(url_for('addSchedule'))

	return render_template('addSchedule.html', form = form)
