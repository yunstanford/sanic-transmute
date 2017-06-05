======
Routes
======

-------
Example
-------

Adding routes follows the standard transmute pattern, with
a decorator converting a function to an aiohttp route:


.. code-block:: python

    from sanic_transmute import describe, add_route
    from sanic import Sanic

    app = Sanic()

    # define a GET endpoint, taking a query parameter integers left and right,
    # which must be integers.
    @describe(paths="/{name}")
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    # append to your route later
    add_route(app, multiply)

the sanic request argument is supported: it will be passed into
any function that has 'request' in it's function signature.

see `transmute-core:function <http://transmute-core.readthedocs.io/en/latest/function.html#functions>`_ for more information on customizing
transmute routes.

-----------------
API Documentation
-----------------

.. autofunction:: sanic_transmute.describe
