Description
===========

Expression is a Domain Specific Language (DSL) designed to express CRUD queries
for Crudity (https://github.com/b3j0f/requester/).

In other words, you can write Crudity Expressions.

Installation
============

.. code-block:: bash

  aptitude install git virtualenv

  git clone https://github.com/J1bz/expression
  git clone https://github.com/b3j0f/requester

  cd expression
  git checkout develop

  virtualenv venv
  source venv/bin/activate

  python setup.py install

  cd ../requester
  git checkout develop
  python setup.py install

  cd ../expression
  python setup.py test

  expression-cli

How-to
======

Quickstart
----------

.. code-block:: python

  >>> from j1bz.expression.interpreter import interpret
  >>> res = interpret("SELECT a;")
  >>> print(repr(res))
  SELECT a

**Note**: ``j1bz.expression.exceptions.ParseError`` should be the only
exception you have to catch when invoking interpret function.

Examples of expressions
-----------------------

CREATE
~~~~~~

.. code-block:: bash

  INSERT VALUES k:v;
  INSERT VALUES k1:v1, k2:v2;
  INSERT INTO i VALUES k:v;
  INSERT VALUES k:v; AS i

**Note**: ``CREATE`` is a synonym of ``INSERT``. It means every time you can
use ``INSERT`` you could have used ``CREATE`` instead (for semantics in some
cases).

READ
~~~~

UPDATE
~~~~~~

DELETE
~~~~~~

**Note**: Expression uses Grako (https://pypi.python.org/pypi/grako) to
generate a parser from a grammar defined in
``etc/j1bz/expression/grammar.bnf``. You can read this bnf description to check
for all available possibilities.
