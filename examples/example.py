from sanic import Sanic
from sanic.response import json
from sanic_transmute import describe, add_route, add_swagger

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


async def test_add_route(request, env: str):
    return json({
        "env": env,
    })


@describe(paths="/api/v1/user/{user}/", methods="GET")
async def test_transmute(request, user: str, env: str=None, group: str=None):
    return {
        "user": user,
        "env": env,
        "group": group,
    }


if __name__ == "__main__":
    add_route(app, test_transmute)
    add_swagger(app, "/api/v1/swagger.json", "/api/v1/")
    app.run(host="0.0.0.0", port=8000)
