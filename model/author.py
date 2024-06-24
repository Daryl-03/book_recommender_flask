from service.db import db

class Author(db.Model):
	db.__tablename__ = 'authors'
	authorId = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	
	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return '<Author %r>' % self.name