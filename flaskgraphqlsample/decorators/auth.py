from functools import wraps

from flask import request
from flask_graphql_auth import verify_jwt_in_argument
from flask_graphql_auth.decorators import _extract_header_token_value
from graphql import GraphQLError


def auth_required(role=None):
    def decorator(fn):
        """
        A decorator to protect a query resolver.

        If you decorate an resolver with this, it will ensure that the requester
        has a valid access token before allowing the resolver to be called. This
        does not check the freshness of the access token.
        """

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                token = _extract_header_token_value(request.headers)

                verify_jwt_in_argument(token)
            except:
                raise GraphQLError("This path requires you to be authenticated.")

            return fn(*args, **kwargs)

        return wrapper

    return decorator
