import graphene
from flask_graphql import GraphQLView


def init_graphql(app):
    """

    :param app: Flask
    """

    from flaskgraphqlsample.graphql.query import Query
    from flaskgraphqlsample.graphql.mutation import Mutation

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=graphene.Schema(query=Query, mutation=Mutation),
            graphiql=app.debug
        )
    )