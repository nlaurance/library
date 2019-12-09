from datetime import datetime
from library.extensions import db


class Book(db.Model):
    """Book is just a title
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return "<Book %s>" % self.title




class BookRequest(db.Model):
    """ A library user requested a book
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
                        nullable=False)
    book = db.relationship('Book',
                           backref=db.backref('requests', lazy=True))

    def __repr__(self):
        return "<BookRequest %s>" % self.id
