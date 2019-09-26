from main_app import db

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	surname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	is_admin = db.Column(db.Boolean(), default=False)
	paper = db.relationship('Papers', backref='proposer', lazy='dynamic')
	schedule = db.relationship('Schedules', backref='speaker', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.surname)

class Papers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(400), index=True)
	url = db.Column(db.String(200), index=True)
	doi = db.Column(db.String(100), index=True)
	proposer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	schedule = db.relationship('Schedules', backref='paper', lazy='dynamic')

	def __repr__(self):
		return '<Paper {}>'.format(self.title)

class Schedules(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date(), index=True, unique=True)
	extra_info = db.Column(db.String(500))
	speaker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))
