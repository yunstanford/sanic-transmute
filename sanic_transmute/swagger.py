from transmute_core.swagger import (
    generate_swagger_html,
    get_swagger_static_root,
    SwaggerSpec
)
import json
from sanic.response import HTTPResponse
from sanic import Blueprint


STATIC_ROOT = "/_swagger/static"
SWAGGER_KEY = "_sanic_transmute_swagger"


def get_swagger_spec(app):
    if not hasattr(app, SWAGGER_KEY):
        setattr(app, SWAGGER_KEY, SwaggerSpec())
    return getattr(app, SWAGGER_KEY)


def add_swagger(app, json_route, html_route):
    """
    a convenience method for both adding a swagger.json route,
    as well as adding a page showing the html documentation
    """
    app.add_route(create_swagger_json_handler(app), json_route, methods=["GET"])
    add_swagger_api_route(app, html_route, json_route)


def add_swagger_api_route(app, target_route, swagger_json_route):
    """
    mount a swagger statics page.
    app: the sanic app object
    target_route: the path to mount the statics page.
    swagger_json_route: the path where the swagger json definitions is
                        expected to be.
    """
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger_html(
        STATIC_ROOT, swagger_json_route
    ).encode("utf-8")

    async def swagger_ui(request):
        return HTTPResponse(body_bytes=swagger_body, content_type="text/html")

    bp = Blueprint('swagger')
    bp.static(STATIC_ROOT, static_root)

    app.add_route(swagger_ui, target_route, methods=["GET"])
    app.blueprint(bp)


def create_swagger_json_handler(app, **kwargs):
    """
    Create a handler that returns the swagger definition
    for an application.
    This method assumes the application is using the
    TransmuteUrlDispatcher as the router.
    """

    spec = get_swagger_spec(app)
    _add_blueprint_specs(app, spec)
    spec_dict = spec.swagger_definition(**kwargs)
    encoded_spec = json.dumps(spec_dict).encode("UTF-8")

    async def swagger(request):
        return HTTPResponse(
            body_bytes=encoded_spec,
            headers={
                "Access-Control-Allow-Origin": "*"
            },
            content_type="application/json",
        )

    return swagger


def _add_blueprint_specs(app, root_spec):
    for name, blueprint in app.blueprints.items():
        if hasattr(blueprint, SWAGGER_KEY):
            spec = getattr(blueprint, SWAGGER_KEY)
            for path, path_item in spec.paths.items():
                if blueprint.url_prefix:
                    path = blueprint.url_prefix + path
                root_spec.add_path(path, path_item)
