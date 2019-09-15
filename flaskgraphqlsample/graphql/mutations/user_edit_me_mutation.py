import graphene
from flask import current_app
from flask_graphql_auth import get_jwt_identity

from flaskgraphqlsample.decorators.auth import auth_required
from flaskgraphqlsample.models.user import UserType, UserSchema, User


class EditProfileMeInput(graphene.InputObjectType):
    email = graphene.String(requred=False)
    password = graphene.String(required=False)


class EditProfileMeMutation(graphene.Mutation):
    class Arguments:
        input = EditProfileMeInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    @auth_required()
    def mutate(root, info, input=None):
        user_schema = UserSchema()
        user_schema.declared_fields["email"].required = False
        user_schema.declared_fields["password"].required = False

        current_user = get_jwt_identity()
        current_user = User.query.filter(User.id == current_user.get("id")).first()

        user = user_schema.load(input, instance=current_user)
        if current_app.extensions.get("sqlalchemy"):
            current_app.extensions.get("sqlalchemy").db.session.commit()
        return EditProfileMeMutation(
            user=user
        )
