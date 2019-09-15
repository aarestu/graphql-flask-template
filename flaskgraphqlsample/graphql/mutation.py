import graphene

from flaskgraphqlsample.graphql.mutations.auth_mutation import AuthMutation
from flaskgraphqlsample.graphql.mutations.auth_refresh_mutation import RefreshMutation
from flaskgraphqlsample.graphql.mutations.user_edit_me_mutation import EditProfileMeMutation
from flaskgraphqlsample.graphql.mutations.user_register_mutation import RegisterUserMutation


class Mutation(graphene.ObjectType):
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()

    # USER
    register_user = RegisterUserMutation.Field()
    editMe = EditProfileMeMutation.Field()
