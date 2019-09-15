import datetime

import click
import flask_sqlalchemy
from flask import current_app
from mimesis import Person, locales

from flaskgraphqlsample.cli.datadb import datadb_cli
from flaskgraphqlsample.cli.utils.progress_bar import print_progress_bar
from flaskgraphqlsample.models.user import User


@datadb_cli.command("random-generator")
@click.argument('count', type=int)
def generate_random_data(count):
    db = flask_sqlalchemy.get_state(current_app).db
    User.query.delete(synchronize_session='evaluate')
    for x in range(count):
        p = Person(locales.EN)

        date_created = datetime.datetime.now() - datetime.timedelta(days=p.work_experience() * 365)
        user = User(email=p.email(), password="1234", date_created=date_created)
        user.set_password(user.password)
        db.session.add(user)
        print_progress_bar(x+1, count, prefix='Progress:', suffix='Complete', length=50)
        if x % 10 == 0:
            db.session.commit()

    db.session.commit()