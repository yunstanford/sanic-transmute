from transmute_core import TransmuteFunction, default_context
from .handler import create_handler
from .swagger import get_swagger_spec


def add_route(app_or_blueprint, fn, context=default_context):
    """
    a decorator that adds a transmute route to the application
    """
    transmute_func = TransmuteFunction(
        fn,
        args_not_from_request=["request"]
    )
    handler = create_handler(transmute_func, context=context)
    get_swagger_spec(app_or_blueprint).add_func(transmute_func, context)
    for p in transmute_func.paths:
        sanic_path = _convert_to_sanic_path(p)
        app_or_blueprint.add_route(handler, sanic_path, methods=list(transmute_func.methods))


def _convert_to_sanic_path(path):
    """
    convert based on route syntax.
    """
    return path.replace("{", "<").replace("}", ">")
