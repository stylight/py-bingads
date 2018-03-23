.. python-bindads documentation master file, created by
   sphinx-quickstart on Fri Mar 23 14:06:49 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-bindads's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Python wrapper for the `BingAds Python SDK <https://github.com/BingAds/BingAds-Python-SDK/>`_
which interacts with Bing Ads API web services. This library's goal is to make a more Pythonic version of the
BingAds Python SDK. Extensions and pull requests are encouraged and welcome.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Releases
--------

Information about releases and changes with versions can be found in the
`release history <https://github.com/stylight/python-bingads/blob/master/HISTORY.rst>`_.

Dependencies
------------

* bingads
* six

Installation
------------

::

    pip install py-bingads

Usage
-----

.. code-block:: python

    >>> from py_bingads.services import BingAds

Running tests & coverage
------------------------

The whole test suite is run by:

::

    inv test

To run a single test just run `py.test -vv --doctest-modules
tests/.../test_something.py` inside the virtual env.

The code coverage is stored in `.coverage` (pickled) and in the \_coverage/
directory (HTML).

The HTML coverage report can then be opened in a browser by:

::

    open _coverage/index.html

Documentation
-------------

[to do]

Contributing
------------

    "If you want to go fast, go alone. If you want to go far, go together."
    -- African proverb

We would love for you to contribute! Please read through our
`contributing guidelines <https://github.com/stylight/python-bingads/blob/master/CONTRIBUTING.rst>`_.

Code of Conduct
---------------
Collaboration is happiest and most fruitful when people work with one another in a compassionate manner.
Please take a few moments to read through our
`code of conduct <https://github.com/stylight/python-bingads/blob/master/CODE_OF_CONDUCT.rst>`_ before contributing.