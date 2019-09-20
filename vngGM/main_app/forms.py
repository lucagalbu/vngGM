from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email
from wtforms.fields.html5 import DateField
from main_app.models import Users, Papers
from flask import flash
from sqlalchemy import and_, or_

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
	speaker = StringField('Speaker', validators=[DataRequired()])
	date = DateField('Date', validators=[DataRequired()])
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
		if not title_empty:
			paper = Papers.query.filter(or_(Papers.title==self.paper_title.data, Papers.doi==self.paper_doi.data)).first()
			if paper is not None:
				raise ValidationError('This paper has already been proposed.')

