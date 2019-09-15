import flask_bcrypt
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from marshmallow import fields, validate, pre_load, ValidationError

from flaskgraphqlsample import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), index=True, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    roles = db.Column(db.Text,
                      index=False,
                      unique=False,
                      nullable=False,
                      default="user")

    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password)

    @staticmethod
    def generate_password_hash(password):
        return flask_bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def create_save(self):
        db.session.add(self)
        db.session.commit()


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        exclude_fields = ("password",)


class UserRole(graphene.Enum):
    ADMIN = "admin"
    USER = "user"


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

    def get_instence(self):
        return self.instance

    email = fields.Str(required=True, validate=[
        validate.Length(min=4, max=250),
        validate.Email()
    ])

    password = fields.Str(required=True, validate=[
        validate.Length(min=4, max=250)
    ])

    @pre_load
    def pre_load(self, data, **kwargs):
        if self.instance:
            if data.get("email"):
                if User.query \
                        .filter(User.id != self.instance.id) \
                        .filter(User.email == data.get("email")).count():
                    raise ValidationError(
                        "{} ready been registered as a user".format(data.get("email")),
                        field_name="email")

        elif data.get("email"):
            if User.query \
                    .filter(User.email == data.get("email")).count():
                raise ValidationError(
                    "{} ready been registered as a user".format(data.get("email")),
                    field_name="email")

        if data.get("password"):
            data["password"] = User.generate_password_hash(data.get("password"))
        return data
