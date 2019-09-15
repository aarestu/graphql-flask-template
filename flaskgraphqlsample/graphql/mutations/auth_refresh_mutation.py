import graphene
from flask_graphql_auth import mutation_header_jwt_refresh_token_required, get_jwt_identity, create_access_token


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        pass

    new_token = graphene.String()

    @classmethod
    @mutation_header_jwt_refresh_token_required
    def mutate(cls, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))