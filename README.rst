sanic-transmute
==================

.. image:: https://travis-ci.org/yunstanford/sanic-transmute.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/yunstanford/sanic-transmute

.. image:: https://coveralls.io/repos/github/yunstanford/sanic-transmute/badge.svg?branch=master
    :alt: coverage status
    :target: https://coveralls.io/github/yunstanford/sanic-transmute?branch=master


A Sanic extension that generates APIs from python function and classes.

You can find out more here:

http://sanic-transmute.readthedocs.io/en/latest/


-------------------------
What is sanic-transmute ?
-------------------------

A `transmute
<http://transmute-core.readthedocs.io/en/latest/index.html>`_
framework for `sanic <http://sanic.readthedocs.io/en/latest/>`_. This
framework provides:

* declarative generation of http handler interfaces by parsing function annotations
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects, using `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* autodocumentation of all handlers generated this way, via `swagger <http://swagger.io/>`_.
