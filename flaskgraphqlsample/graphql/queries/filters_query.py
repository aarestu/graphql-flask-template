import graphene
from sqlalchemy import func
from sqlalchemy.sql import sqltypes

from flaskgraphqlsample.decorators.auth import auth_required
from flaskgraphqlsample.graphql.sqlalchemy_connection_field import SQLAlchemyConnectionField


class FilterQuery(SQLAlchemyConnectionField):

    def __init__(self, t, *args, **kwargs):
        model = t._meta.model
        fields = t._meta.fields
        for field in fields:

            if isinstance(model.__dict__[field].type, sqltypes.String):
                kwargs.setdefault(field + "_is_like", graphene.String())
                kwargs.setdefault(field + "_is_ne", graphene.String())
                kwargs.setdefault(field + "_is_eq", graphene.String())

            if isinstance(model.__dict__[field].type, sqltypes.Integer):
                kwargs.setdefault(field + "_is_gte", graphene.Int())
                kwargs.setdefault(field + "_is_gt", graphene.Int())
                kwargs.setdefault(field + "_is_lt", graphene.Int())
                kwargs.setdefault(field + "_is_lte", graphene.Int())
                kwargs.setdefault(field + "_is_ne", graphene.Int())
                kwargs.setdefault(field + "_is_eq", graphene.Int())

            if isinstance(model.__dict__[field].type, sqltypes.Numeric):
                kwargs.setdefault(field + "_is_gte", graphene.Float())
                kwargs.setdefault(field + "_is_gt", graphene.Float())
                kwargs.setdefault(field + "_is_lt", graphene.Float())
                kwargs.setdefault(field + "_is_lte", graphene.Float())
                kwargs.setdefault(field + "_is_ne", graphene.Float())
                kwargs.setdefault(field + "_is_eq", graphene.Float())

            if isinstance(model.__dict__[field].type, sqltypes.DateTime):
                kwargs.setdefault(field + "_is_gte", graphene.DateTime())
                kwargs.setdefault(field + "_is_gt", graphene.DateTime())
                kwargs.setdefault(field + "_is_lt", graphene.DateTime())
                kwargs.setdefault(field + "_is_lte", graphene.DateTime())
                kwargs.setdefault(field + "_is_ne", graphene.DateTime())
                kwargs.setdefault(field + "_is_eq", graphene.DateTime())

        super().__init__(t, *args, **kwargs)

    @classmethod
    @auth_required()
    def get_query(cls, model, info, sort=None, **args):

        query = super().get_query(model, info, sort, **args)
        for filter in args:

            if filter[-len("_is_like"):] == "_is_like" and filter[:len(filter) - len("_is_like")] in model.__dict__:
                field = filter[:len("_is_like") - 1]
                if isinstance(model.__dict__[field].type, sqltypes.String):
                    query = query.filter(model.__dict__[field].like("%{}%".format(args.get(filter))))

            if filter[-len("_is_ne"):] == "_is_ne" and filter[:len(filter) - len("_is_ne")] in model.__dict__:
                field = filter[:len(filter) - len("_is_ne")]
                value = args.get(filter)

                if isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    value = func.datetime(value)

                if isinstance(model.__dict__[field].type, sqltypes.Date):
                    value = func.date(value)

                if isinstance(model.__dict__[field].type, sqltypes.String) \
                        or isinstance(model.__dict__[field].type, sqltypes.Numeric) \
                        or isinstance(model.__dict__[field].type, sqltypes.Integer) \
                        or isinstance(model.__dict__[field].type, sqltypes.Date) \
                        or isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    query = query.filter(model.__dict__[field] != value)

            if filter[-len("_is_eq"):] == "_is_eq" and filter[:len(filter) - len("_is_eq")] in model.__dict__:
                field = filter[:len(filter) - len("_is_eq")]
                value = args.get(filter)

                if isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    value = func.datetime(value)

                if isinstance(model.__dict__[field].type, sqltypes.Date):
                    value = func.date(value)

                if isinstance(model.__dict__[field].type, sqltypes.String) \
                        or isinstance(model.__dict__[field].type, sqltypes.Numeric) \
                        or isinstance(model.__dict__[field].type, sqltypes.Integer) \
                        or isinstance(model.__dict__[field].type, sqltypes.Date) \
                        or isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    query = query.filter(model.__dict__[field] == value)

            if filter[-len("_is_gt"):] == "_is_gt" and filter[:len(filter) - len("_is_gt")] in model.__dict__:
                field = filter[:len(filter) - len("_is_gt")]
                value = args.get(filter)

                if isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    value = func.datetime(value)

                if isinstance(model.__dict__[field].type, sqltypes.Date):
                    value = func.date(value)
                if isinstance(model.__dict__[field].type, sqltypes.Numeric) \
                        or isinstance(model.__dict__[field].type, sqltypes.Integer) \
                        or isinstance(model.__dict__[field].type, sqltypes.Date) \
                        or isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    query = query.filter(model.__dict__[field] > value)

            if filter[-len("_is_gte"):] == "_is_gte" and filter[:len(filter) - len("_is_gte")] in model.__dict__:
                field = filter[:len(filter) - len("_is_gte")]
                if isinstance(model.__dict__[field].type, sqltypes.Numeric) \
                        or isinstance(model.__dict__[field].type, sqltypes.Integer) \
                        or isinstance(model.__dict__[field].type, sqltypes.Date) \
                        or isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    query = query.filter(model.__dict__[field] >= args.get(filter))

            if filter[-len("_is_lt"):] == "_is_lt" and filter[:len(filter) - len("_is_lt")] in model.__dict__:
                field = filter[:len(filter) - len("_is_lt")]
                value = args.get(filter)

                if isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    value = func.datetime(value)

                if isinstance(model.__dict__[field].type, sqltypes.Date):
                    value = func.date(value)
                if isinstance(model.__dict__[field].type, sqltypes.Numeric) \
                        or isinstance(model.__dict__[field].type, sqltypes.Integer) \
                        or isinstance(model.__dict__[field].type, sqltypes.Date) \
                        or isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    query = query.filter(model.__dict__[field] < value)

            if filter[-len("_is_lte"):] == "_is_lte" and filter[:len(filter) - len("_is_lte")] in model.__dict__:
                field = filter[:len(filter) - len("_is_lte")]
                value = args.get(filter)

                if isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    value = func.datetime(value)

                if isinstance(model.__dict__[field].type, sqltypes.Date):
                    value = func.date(value)
                if isinstance(model.__dict__[field].type, sqltypes.Numeric) \
                        or isinstance(model.__dict__[field].type, sqltypes.Integer) \
                        or isinstance(model.__dict__[field].type, sqltypes.Date) \
                        or isinstance(model.__dict__[field].type, sqltypes.DateTime):
                    query = query.filter(model.__dict__[field] >= value)

        return query
