from sanic import Sanic, Blueprint
from sanic.response import json
from sanic_transmute import describe, add_route, add_swagger, APIException
from sanic.exceptions import ServerError
import attr


@attr.s
class User:
    points = attr.ib(type=int)


app = Sanic()
bp = Blueprint("test_blueprints", url_prefix="/blueprint")


@describe(paths="/api/v1/user/{user}/", methods="GET")
async def test_transmute_get(request, user: str, env: str=None, group: [str]=None):
    """
    API Description: Transmute Get. This will show in the swagger page (localhost:8000/api/v1/).
    """
    return {
        "user": user,
        "env": env,
        "group": group,
    }


@describe(paths="/api/v1/user/", methods="POST")
async def test_transmute_post(request, user: User) -> User:
    """
    API Description: Transmute Post. This will show in the swagger page (localhost:8000/api/v1/).
    """
    return user


@describe(paths="/killme")
async def handle_exception(request) -> User:
    """
    API Description: Handle exception. This will show in the swagger page (localhost:8000/api/v1/).
    """
    raise ServerError("Something bad happened", status_code=500)


@describe(paths="/api/v1/user/missing")
async def handle_api_exception(request) -> User:
    """
    API Description: Handle APIException. This will show in the swagger page (localhost:8000/api/v1/).
    """
    raise APIException("Something bad happened", code=404)


@describe(paths="/multiply")
async def get_blueprint_params(request, left: int, right: int) -> str:
    """
    API Description: Multiply, left * right. This will show in the swagger page (localhost:8000/api/v1/).
    """
    res = left * right
    return "{left}*{right}={res}".format(left=left, right=right, res=res)


if __name__ == "__main__":
    add_route(app, test_transmute_get)
    add_route(app, test_transmute_post)
    add_route(app, handle_exception)
    add_route(app, handle_api_exception)
    # register blueprints
    add_route(bp, get_blueprint_params)
    app.blueprint(bp)
    # add swagger
    add_swagger(app, "/api/v1/swagger.json", "/api/v1/")
    app.run(host="0.0.0.0", port=8000)