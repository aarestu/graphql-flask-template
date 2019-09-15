import graphene
from flask_graphql_auth import get_jwt_identity

from flaskgraphqlsample.decorators.auth import auth_required
from flaskgraphqlsample.models.user import UserType, User


class MeQuery(graphene.Field):
    def __init__(self):
        super(MeQuery, self).__init__(UserType, resolver=self.me)

    @auth_required()
    def me(self, *args, **kwargs):
        current_user = get_jwt_identity()

        return User.query.filter(User.id == current_user.get("id")).first()
