.. sanic-transmute documentation master file, created by
   sphinx-quickstart on Wed Aug 17 13:50:33 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sanic-transmute
===============

.. image:: https://travis-ci.org/yunstanford/sanic-transmute.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/yunstanford/sanic-transmute

.. image:: https://coveralls.io/repos/github/yunstanford/sanic-transmute/badge.svg?branch=master
    :alt: coverage status
    :target: https://coveralls.io/github/yunstanford/sanic-transmute?branch=master


A transmute implementation for sanic. 


-------------------------
What is sanic-transmute ?
-------------------------

a Sanic extension that generates APIs from python function and classes. 


----------------------
Quick start
----------------------

Let's get started.

.. code::

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




Contents:

.. toctree::
   :maxdepth: 2

   installation
   example
   routes
   serialization
   autodocumentation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
