Description
===========

Expression is a Domain Specific Language (DSL) designed to express CRUD queries
for b3j0f.crudity (https://github.com/b3j0f/requester/).

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

.. code-block:: bash

  SELECT ALL;
  SELECT s;
  SELECT s WHERE w;
  SELECT s GROUP BY g;
  SELECT s ORDER BY o;
  SELECT s LIMIT 10;
  SELECT s; AS mys

  SELECT s WHERE wh GROUP BY g ORDER BY o LIMIT 10; AS mys

  SELECT a, b, c;
  SELECT f();
  SELECT f(a, b, c);

  SELECT s WHERE (a);
  SELECT s WHERE (a = b);
  SELECT s WHERE (a != b);
  SELECT s WHERE (a > b);
  SELECT s WHERE (a >= b);
  SELECT s WHERE (a < b);
  SELECT s WHERE (a <= b);
  SELECT s WHERE (a IN b);
  SELECT s WHERE (a NIN b);
  SELECT s WHERE (a LIKE b);

  SELECT s WHERE (a AND b);
  SELECT s WHERE (a OR b);
  SELECT s WHERE (a OR (b AND c));

  SELECT s ORDER BY o1, o2;
  SELECT s ORDER BY o1 DESC, o2, o3 ASC;

**Note**: ``READ`` is a synonym of ``SELECT``.

UPDATE
~~~~~~

.. code-block:: bash

  UPDATE VALUES k:v;
  UPDATE VALUES k:v WHERE w;
  UPDATE VALUES k:v; AS myu

  UPDATE INTO u VALUES k:v;
  UPDATE INTO u VALUES k:v WHERE w;
  UPDATE INTO u VALUES k1:v1, k2:v2;

DELETE
~~~~~~

.. code-block:: bash

  DELETE d;
  DELETE d1, d2, d3;
  DELETE d WHERE w;
  DELETE d1, d2, d3 WHERE w;
  DELETE d; AS myd

**Note**: Expression uses Grako (https://pypi.python.org/pypi/grako) to
generate a parser from a grammar defined in
``j1bz/expression/etc/j1bz/expression/grammar.bnf``. You can read this bnf
description to check for all available possibilities.
