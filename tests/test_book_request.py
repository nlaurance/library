import factory
from pytest_factoryboy import register

from library.models import Book, BookRequest


@register
class BookFactory(factory.Factory):
    title = factory.Sequence(lambda n: "Boring stories volume:%d" % n)

    class Meta:
        model = Book


def test_get_book_request(client, db, book, book_request):
    # test 404
    rep = client.get("/api/v1/request/100000",
                     headers={"content-type": "application/json"})
    assert rep.status_code == 404

    db.session.add(book)
    db.session.commit()
    db.session.add(book_request)
    db.session.commit()

    # test 200
    rep = client.get("/api/v1/request/%d" % book_request.id,
                     headers={"content-type": "application/json"})
    assert rep.status_code == 200

    data = rep.get_json()
    assert data["email"] == 'me@myself.com'
    assert data["title"] == 'Boring stories volume:1'


def test_del_book_request(client, db, book, book_request):
    db.session.add(book)
    db.session.commit()
    db.session.add(book_request)
    db.session.commit()

    rep = client.get("/api/v1/request/1",
                     headers={"content-type": "application/json"})
    assert rep.status_code == 200

    # pouf!
    rep = client.delete("/api/v1/request/1",
                     headers={"content-type": "application/json"})
    assert rep.status_code == 200

    # it's gone
    rep = client.get("/api/v1/request/1",
                     headers={"content-type": "application/json"})
    assert rep.status_code == 404


def test_create_book_request(client, db, book):
    # test bad data
    data = {"title": "Boring stories volume:1"}
    rep = client.post("/api/v1/request", json=data,
                      headers={"content-type": "application/json"})
    assert rep.status_code == 422

    db.session.add(book)
    db.session.commit()

    data = {"title": "Fascinating stories volume:1",
            "email": "me@myself.com"}

    rep = client.post("/api/v1/request", json=data,
                      headers={"content-type": "application/json"})
    assert rep.status_code == 400

    data = {"title": book.title,
            "email": "me@myself.com"}

    rep = client.post("/api/v1/request", json=data,
                      headers={"content-type": "application/json"})
    assert rep.status_code == 201

    data = rep.get_json()
    book_request = db.session.query(BookRequest).filter_by(id=data["id"]).first()

    assert book_request.email == "me@myself.com"
    assert book_request.book_id == book.id


def test_get_all_book_requests(client, db, book, book_request):
    db.session.add(book)
    db.session.commit()
    book_requests = [BookRequest(
        email="user_%d" % i,
        book_id=book.id
    ) for i in range(5)]
    db.session.add_all(book_requests)
    db.session.commit()

    rep = client.get("/api/v1/request",
                     headers={"content-type": "application/json"})
    assert rep.status_code == 200

    results = rep.get_json()
    for book_request in book_requests:
        assert any(u["id"] == book_request.id for u in results)
