from flask import request
from flask_restful import Resource

from library.extensions import ma, db
from library.models import Book, BookRequest


class BookSchema(ma.ModelSchema):
    id = ma.Int(dump_only=True)
    title = ma.String(required=True)

    class Meta:
        model = Book
        sqla_session = db.session


class BookRequestSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    title = ma.String(required=True)
    email = ma.Email(required=True)
    timestamp = ma.String(dump_only=True)


class BookRequestList(Resource):
    """Creation and get_all
    """

    def get(self):
        book_request_data = db.session.query(
            BookRequest.email, BookRequest.id, BookRequest.timestamp, Book.title
        ).join(Book, BookRequest.book_id == Book.id)
        schema = BookRequestSchema()
        return schema.dump(book_request_data, many=True).data

    def post(self):
        schema = BookRequestSchema()
        book_request_data, errors = schema.load(request.json)
        if errors:
            return errors, 422

        book = (
            db.session.query(Book)
            .filter(Book.title == book_request_data["title"])
            .first()
        )
        if book is None:
            return {"error": "unknown title"}, 400

        book_request = BookRequest(email=book_request_data["email"], book_id=book.id)
        db.session.add(book_request)
        db.session.commit()
        book_request.title = book.title

        return schema.dump(book_request).data, 201


class BookRequestResource(Resource):
    """
    unit get, and deletion
    """
    def get(self, request_id):
        schema = BookRequestSchema()
        book_request = BookRequest.query.get_or_404(request_id)
        book_request.title = book_request.book.title
        return schema.dump(book_request).data

    def delete(self, request_id):
        book_request = BookRequest.query.get_or_404(request_id)
        db.session.delete(book_request)
        db.session.commit()
        return
