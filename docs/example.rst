=======
Example
=======

A simple example.

.. code-block:: python

    from sanic import Sanic, Blueprint
    from sanic.response import json
    from sanic_transmute import describe, add_route, add_swagger, APIException
    from sanic.exceptions import ServerError
    from schematics.models import Model
    from schematics.types import IntType


    class User(Model):
        points = IntType()


    app = Sanic()
    bp = Blueprint("test_blueprints", url_prefix="/blueprint")


    @describe(paths="/api/v1/user/{user}/", methods="GET")
    async def test_transmute(request, user: str, env: str=None, group: [str]=None):
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


    @describe(paths="/multiply")
    async def get_blueprint_params(request, left: int, right: int) -> str:
        res = left * right
        return "{left}*{right}={res}".format(left=left, right=right, res=res)


    if __name__ == "__main__":
        add_route(app, test_transmute)
        add_route(app, handle_exception)
        add_route(app, handle_api_exception)
        # register blueprints
        add_route(bp, get_blueprint_params)
        app.blueprint(bp)
        # add swagger
        add_swagger(app, "/api/v1/swagger.json", "/api/v1/")
        app.run(host="0.0.0.0", port=8000)
