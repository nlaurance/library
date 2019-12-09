import click
from flask.cli import FlaskGroup

from library.app import create_app


def create_library(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_library)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from library.extensions import db
    from library.models import User, Book

    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")

    click.echo("create books")
    db.session.add_all(
        [
            Book(title=title)
            for title in (
                "Alice au pays des merveilles",
                "أليس في بلاد العجائب",
                "Troioù-kaer Alis e Bro ar Marzhoù",
                "אליס בארץ הפלאות",
                "Eachtraí Eilíse i dTír na nIontas",
                "Alice in Wondeland",
                "Dracula",
                "Ulysses",
                "Dubliners",
            )
        ]
    )

    db.session.commit()
    click.echo("created some titles")


if __name__ == "__main__":
    cli()
