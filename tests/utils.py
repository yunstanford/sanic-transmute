from sanic import Sanic
from sanic.response import json
from sanic_transmute import describe, add_route, add_swagger


@describe(paths="/api/v1/user/{user}/", methods="GET")
async def test_transmute(request, user: str, env: str=None, group: str=None):
    return {
        "user": user,
        "env": env,
        "group": group,
    }


def create_app():
    app = Sanic()
    add_route(app, test_transmute)
    add_swagger(app, "/api/v1/swagger.json", "/api/v1/")
    return app