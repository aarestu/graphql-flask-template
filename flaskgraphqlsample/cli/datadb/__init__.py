from flask.cli import AppGroup

datadb_cli = None


def init_cli(app):
    global datadb_cli
    datadb_cli = AppGroup('datadb')

    from flaskgraphqlsample.cli.datadb import generate_random

    app.cli.add_command(datadb_cli)
