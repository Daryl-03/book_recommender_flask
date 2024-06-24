from service.db import db

class Genre(db.Model):
	db.__tablename__ = 'genres'
	genreId = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	
	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return '<Genre %r>' % self.name