from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email
from wtforms.fields.html5 import DateField
from main_app.models import Users, Papers, Schedules
from flask import flash
from datetime import timedelta
from sqlalchemy import and_, or_, desc

class AddUser(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	surname = StringField('Surname', validators=[DataRequired()])
	email = StringField('E-mail', validators=[DataRequired(), Email()])
	submit = SubmitField('Add User')

	def validate_name(self, name):
		user = Users.query.filter(and_(Users.name==self.name.data, Users.surname==self.surname.data)).first()
		if user is not None:
			raise ValidationError('There is already a user with the same name and surname.')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('The given email is already in use.')


class AddSchedule(FlaskForm):
	#Find the next user (Look at user list and select the ones with the next id)
	current_user_id = Users.query.join(Schedules).order_by(desc('date')).first().id
	if current_user_id == Users.query.order_by(desc('id')).first().id:
		current_user_id == Users.query.order_by('id').first().id
	next_user = Users.query.order_by(Users.id).filter(Users.id > current_user_id).first()
	

	#Find the next Thursday
	current_day = Schedules.query.order_by(desc('date')).first().date
	next_thursday = current_day + timedelta(7) if current_day.weekday() == 3 else current_day + timedelta((3-current_day.weekday()) % 7 )
	
	speaker = StringField('Speaker', validators=[DataRequired()], default = next_user.name)
	date = DateField('Date', validators=[DataRequired()], default = next_thursday)
	paper_title = StringField('Paper')
	paper_doi = StringField('Paper doi')
	paper_url = StringField('Paper url')
	paper_proposer = StringField('Paper proposer')
	discussion = StringField('Discussion topic')
	submit = SubmitField('Add Schedule')

	#If paper_doi or paper_url are given, paper_title cannot be empty
	#Check if paper already been proposed
	def validate_paper_title(self, paper_title):
		doi_url_not_empty = (self.paper_doi.data != '') or (self.paper_url.data !=  '')
		title_empty = self.paper_title.data == ''
		if doi_url_not_empty and title_empty:
				raise ValidationError('A doi or a url cannot be provided without a title for the paper.')
		
