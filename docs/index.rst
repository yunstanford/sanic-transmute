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
