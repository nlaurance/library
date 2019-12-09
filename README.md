# library

install

pip install -r requirements.txt


run tests

DATABASE_URI=sqlite:///:memory: SECRET_KEY=testing FLASK_ENV=development pytest tests

or

tox

run


DATABASE_URI=sqlite:////tmp/library.db SECRET_KEY=testing FLASK_ENV=development library run


# Docker

build

sudo docker build -t library .

run

sudo docker run --rm --env-file .flaskenv -p 5000:5000 library:latest library run -h 0.0.0.0


endpoints at /api/v1

/api/v1/request
...


