import pytest
from sanic import Sanic
from sanic_transmute import (
    describe, add_swagger, add_route, route,
    APIException
)
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError
from .utils import User


@pytest.fixture
def app():
    app = Sanic('sanic_test_app')

    # Handlers
    async def hello_world(request):
        return HTTPResponse(body="Hello World")

    @describe(paths="/api/v1/user/{user}", methods="GET")
    async def get_path_parameters(request, user: str) -> str:
        return user

    @describe(paths="/api/v1/env/", methods="GET")
    async def get_parameters_optional(request, exist: bool=False) -> bool:
        return exist

    @describe(paths="/multiply")
    async def get_query_parameters(request, left: int, right: int) -> int:
        return left * right

    @describe(paths="/killme")
    async def handle_exceptions(request) -> User:
        raise ServerError("Something bad happened", status_code=500)

    @describe(paths="/api/v1/user/missing")
    async def handle_api_exception(request) -> User:
        raise APIException("Something bad happened", code=404)

    # Routes
    app.add_route(hello_world, "/", methods=["GET"])
    add_route(app, get_path_parameters)
    add_route(app, get_parameters_optional)
    add_route(app, get_query_parameters)
    add_route(app, handle_exceptions)
    add_route(app, handle_api_exception)

    return app