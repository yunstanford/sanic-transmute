from sanic import Sanic
from sanic.response import json
from sanic_transmute import describe, add_route, add_swagger, APIException
from sanic.exceptions import ServerError
from schematics.models import Model
from schematics.types import IntType


class User(Model):
    points = IntType()


app = Sanic()


@app.route("/<path_param>/")
async def test(request, path_param):
    return json(
        {
            "path_params": request.app.router.get(request)[2],
            "header_params": request.headers,
            "query_params": request.args,
            "body": request.body,
        }
    )


@describe(paths="/api/v1/user/{user}/", methods="GET")
async def test_transmute(request, user: str, env: str=None, group: str=None):
    return {
        "user": user,
        "env": env,
        "group": group,
    }


@describe(paths="/killme")
async def handle_exception(request) -> User:
    raise ServerError("Something bad happened", status_code=500)


@describe(paths="/api/v1/user/missing")
async def handle_api_exception(request) -> User:
    raise APIException("Something bad happened", code=404)


if __name__ == "__main__":
    add_route(app, test_transmute)
    add_route(app, handle_exception)
    add_route(app, handle_api_exception)
    add_swagger(app, "/api/v1/swagger.json", "/api/v1/")
    app.run(host="0.0.0.0", port=8000)
