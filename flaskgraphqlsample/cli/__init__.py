from flaskgraphqlsample.cli import datadb


def init_cli(app):
    datadb.init_cli(app)
