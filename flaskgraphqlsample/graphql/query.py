import graphene
from graphene import relay

from flaskgraphqlsample.graphql.queries.filters_query import FilterQuery
from flaskgraphqlsample.graphql.queries.me_query import MeQuery
from flaskgraphqlsample.models.user import UserType


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    users = FilterQuery(UserType)

    me = MeQuery()
