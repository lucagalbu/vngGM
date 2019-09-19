from main_app import app, db
from main_app.forms import AddUser, AddSchedule
from flask import render_template, flash, redirect, url_for
from main_app.models import Users

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Tmp')

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
	form.validate_on_submit()
	return render_template('addSchedule.html', form = form)
