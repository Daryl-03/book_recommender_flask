from service.db import db

class Rating(db.Model):
	db.__tablename__ = 'ratings'
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.Integer, nullable=False)
	bookId = db.Column(db.String(100), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	
	def __init__(self, userId, bookId, rating):
		self.userId = userId
		self.bookId = bookId
		self.rating = rating
		
	def __repr__(self):
		return '<Rating %r>' % self.id