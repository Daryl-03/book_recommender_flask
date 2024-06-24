from service.db import db

class UserHistory(db.Model):
	db.__tablename__ = 'user_history'
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.Integer, nullable=False)
	bookId = db.Column(db.String(100), nullable=False)
	bookState = db.Column(db.String(20), nullable=False)
	bookmark = db.Column(db.Integer, nullable=False)
	timestamp = db.Column(db.Integer, nullable=False)
	
	def __init__(self, userId, bookId, bookStateId, bookmark, timestamp):
		self.userId = userId
		self.bookId = bookId
		self.bookStateId = bookStateId
		self.bookmark = bookmark
		self.timestamp = timestamp
		
	def __repr__(self):
		return '<UserHistory %r>' % self.id