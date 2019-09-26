from main_app import app, db
from main_app.forms import AddUser, AddSchedule
from flask import render_template, flash, redirect, url_for
from main_app.models import Users, Papers, Schedules
from sqlalchemy.orm import aliased
from sqlalchemy import desc

@app.route('/')
@app.route('/index')
def index():	
	user1, user2 = aliased(Users, name='user_schedule'), aliased(Users, name='user_paper')
	schedules = db.session.query(Schedules, user1, user2, Papers) \
	.join(user1, user1.id==Schedules.speaker_id, isouter=True) \
	.join(Papers, Papers.id==Schedules.paper_id, isouter=True) \
	.join(user2, user2.id==Papers.proposer_id, isouter=True) \
	.order_by(desc('date')).all()

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
	users = Users.query.order_by('id').all()
	return render_template('listUsers.html', users=users)

@app.route('/addSchedule', methods = ['POST', 'GET'])
def addSchedule():
	form = AddSchedule()

	if form.validate_on_submit():
		if form.paper_title.data is not "":
			user=Users.query.filter_by(name=form.paper_proposer.data).first()
			user_id = user.id if user is not None else None
			paper = Papers(title=form.paper_title.data, url=form.paper_url.data, doi=form.paper_doi.data, proposer_id=user_id)
			db.session.add(paper)

		added_paper=Papers.query.filter_by(title=form.paper_title.data).first()
		user=Users.query.filter_by(name=form.speaker.data).first()
		user_id = user.id if user is not None else None
		added_paper_id = added_paper.id if added_paper is not None else None
		schedule = Schedules(speaker_id=user_id, date=form.date.data, extra_info=form.discussion.data, paper_id=added_paper_id)
		db.session.add(schedule)

		db.session.commit()
		return redirect(url_for('addSchedule'))

	return render_template('addSchedule.html', form = form)
