import pytest
from sanic import Sanic, Blueprint
from sanic_transmute import (
    describe, add_swagger, add_route, route,
    APIException,
    Response
)
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError
from .utils import User
from schematics.types import ListType, StringType


@pytest.fixture
def app():
    app = Sanic('sanic_test_app')

    # App Handlers
    async def hello_world(request):
        return HTTPResponse(body="Hello World")

    @describe(paths="/api/v1/user/{user}", methods="GET")
    async def get_path_parameters(request, user: str) -> str:
        return user

    @describe(paths="/api/v1/group/", methods="GET")
    async def get_path_parameters_list(request, group: [str]=None) -> str:
        if not group:
            group = []
        group = sorted(group)
        return ",".join(group)

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

    @describe(paths="/api/v1/headers/",
              response_types={
                  200: {
                      "type": str,
                      "description": "success",
                      "headers": {
                          "location": {
                              "description": "url to the location",
                              "type": str
                          }
                      }
                  }
              })
    async def get_headers(request):
        return Response(
                "headers",
                headers={"location": "foooo"},
            )

    @describe(
        paths="/body_and_header",
        methods="POST",
        body_parameters=["body"],
        header_parameters=["header"]
    )
    async def body_and_header_params(request, body: str, header: str) -> bool:
        return body == header

    # Routes
    app.add_route(hello_world, "/", methods=["GET"])
    add_route(app, get_path_parameters)
    add_route(app, get_parameters_optional)
    add_route(app, get_path_parameters_list)
    add_route(app, get_query_parameters)
    add_route(app, handle_exceptions)
    add_route(app, handle_api_exception)
    add_route(app, get_headers)
    add_route(app, body_and_header_params)

    # Blueprints
    @describe(paths="/multiply")
    async def get_blueprint_params(request, left: int, right: int) -> str:
        res = left * right
        return "{left}*{right}={res}".format(left=left, right=right, res=res)

    bp = Blueprint("test_blueprints", url_prefix="/blueprint")
    add_route(bp, get_blueprint_params)
    app.blueprint(bp)

    # Swagger
    add_swagger(app, "/api/v1/swagger.json", "/api/v1/")

    return app
