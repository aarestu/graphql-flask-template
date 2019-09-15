from graphene_sqlalchemy import SQLAlchemyConnectionField as SQLAlchemyConnectionFieldBase


class SQLAlchemyConnectionField(SQLAlchemyConnectionFieldBase):
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    @classmethod
    def connection_resolver(cls, resolver, connection_type, model, root, info, **args):
        args = cls.validate_first_last(args)
        return super(SQLAlchemyConnectionField, cls) \
            .connection_resolver(resolver, connection_type, model, root, info, **args)

    @classmethod
    def validate_first_last(cls, args):
        request_row = None
        if 'first' in args and type(args.get("first")) == int \
                and 'last' in args and type(args.get("last")) == int:

            request_row = min(args.get("first"), args.get("last"))
        elif 'first' in args and type(args.get("first")) == int:
            request_row = args.get("first")
        elif 'last' in args and type(args.get("last")) == int:
            request_row = args.get("last")

        if request_row and request_row > cls.MAX_PAGE_SIZE:
            raise ValueError('request row must not be greater than {}.'.format(
                cls.MAX_PAGE_SIZE
            ))

        if request_row == None and not args.get("first"):
            args['first'] = cls.DEFAULT_PAGE_SIZE

        return args
