import graphene

from flaskgraphqlsample.models.user import UserType, UserRole, UserSchema, User


class RegisterUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    roles = UserRole()


class RegisterUserMutation(graphene.Mutation):
    class Arguments:
        input = RegisterUserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        user_schema = UserSchema()

        user = user_schema.load(input)
        user.create_save()
        return RegisterUserMutation(
            user=User.query.filter(User.email == input.get("email")).first()
        )

