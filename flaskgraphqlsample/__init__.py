from flask import Flask
from flask_graphql_auth import GraphQLAuth
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flaskgraphqlsample.cli import init_cli
from flaskgraphqlsample.graphql import init_graphql

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    global db, ma

    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    ma.init_app(app)

    Migrate(app, db)

    GraphQLAuth(app)

    init_graphql(app)
    init_cli(app)
    return app
