from main_app import app, db
from main_app.forms import AddUser, AddSchedule
from flask import render_template, flash, redirect, url_for
from main_app.models import Users, Papers, Schedules
from sqlalchemy.orm import aliased
from sqlalchemy import desc
from datetime import timedelta, datetime


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
	else:
		#Find the next user (Look at user list and select the ones with the next id)
		current_user = Users.query.join(Schedules).order_by(desc('date')).first()
		
		if(current_user is None): #This happens if the schedule is empty
			current_user_id = Users.query.order_by('id').first().id
		else:
			current_user_id = current_user.id
		#If we have reached the bottom of the user list, start from the top again
		if current_user_id == Users.query.order_by(desc('id')).first().id:
			current_user_id == Users.query.order_by('id').first().id
		next_user = Users.query.order_by(Users.id).filter(Users.id > current_user_id).first()
			
		#Find the next Thursday
		current_day = Schedules.query.order_by(desc('date')).first()
		if current_day is None: #This happens if the schedule is empty
			current_day = datetime.now()
		else:
			current_day = current_day.date
		next_thursday = current_day + timedelta(7) if current_day.weekday() == 3 else current_day + timedelta((3-current_day.weekday()) % 7 )

		#Set the default user and date
		form.date.default=next_thursday
		form.speaker.default=next_user.name
		form.process()

	return render_template('addSchedule.html', form = form)
