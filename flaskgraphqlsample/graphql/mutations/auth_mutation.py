import graphene
from flask_graphql_auth import create_access_token, create_refresh_token
from graphql import GraphQLError

from flaskgraphqlsample.models.user import User


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, email, password):

        user = User.query.filter(User.email == email).first()
        if not user:
            raise GraphQLError("Incorrect email or password.")
        if not user.check_password(password):
            raise GraphQLError("Incorrect email or password.")

        return AuthMutation(
            access_token=create_access_token({"id": user.id}),
            refresh_token=create_refresh_token({"id": user.id}),
        )
