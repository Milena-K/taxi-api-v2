#!/usr/bin/env python3
from urllib.parse import (
    parse_qs,
)
from channels.middleware import (
    BaseMiddleware,
)
from django.contrib.auth.models import (
    AnonymousUser,
)
from django.contrib.auth import (
    get_user_model,
)
import rest_framework_simplejwt as jwt
from rest_framework_simplejwt.tokens import (
    AccessToken,
)
from rest_framework import (
    exceptions as rest_exceptions,
)
from jwt import (
    exceptions as jwt_exceptions,
)

from channels.db import (
    database_sync_to_async,
)

User = get_user_model()


@database_sync_to_async
def get_user_from_token(
    token,
):
    try:
        access_token_obj = (
            AccessToken(token)
        )
        user_id = (
            access_token_obj[
                "user_id"
            ]
        )
        user = (
            User.objects.get(
                pk=user_id
            )
        )
        return user
    except jwt_exceptions.ExpiredSignatureError:
        raise rest_exceptions.AuthenticationFailed(
            "Token Expired, Please Login"
        )
    except jwt_exceptions.DecodeError:
        raise rest_exceptions.AuthenticationFailed(
            "Token Modified by thirdparty"
        )
    except jwt_exceptions.InvalidTokenError:
        raise rest_exceptions.AuthenticationFailed(
            "Invalid Token"
        )
    except Exception as e:
        raise rest_exceptions.AuthenticationFailed(
            e
        )


class TokenAuthMiddleware(
    BaseMiddleware
):
    async def __call__(
        self,
        scope,
        receive,
        send,
    ):
        query_string = parse_qs(
            scope[
                "query_string"
            ].decode()
        )
        token = (
            query_string.get(
                "token",
                [None],
            )[0]
        )
        scope[
            "user"
        ] = await get_user_from_token(
            token
        )
        return await super().__call__(
            scope,
            receive,
            send,
        )
