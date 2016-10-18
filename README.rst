Summary
=======

* `Description`_

  * `Crudity expressions, cool ! But... what is it ?`_

* `Installation`_
* `How-to`_

  * `Quickstart`_
  * `Examples of expressions`_ 

    * `CREATE`_
    * `READ`_
    * `UPDATE`_
    * `DELETE`_

* `Advanced how-to`_

  * `Using a custom grammar`_
  * `Interpreter vs interpret`_
  * `Exception handling`_

Description
===========

Expression is a Domain Specific Language (DSL) designed to express CRUD queries
for ``b3j0f.crudity`` (https://github.com/b3j0f/requester/).

In other words, you can write Crudity Expressions.

Crudity expressions, cool ! But... what is it ?
-----------------------------------------------

This package has been designed to work in strong coupling with
``b3j0f.requester``, so you should know what it is before continuing.

In ``b3j0f.requester``, everything is an ``Expression`` (``E``) or a
``Function`` (``F``). If you want to compare ``a`` and ``b`` you need to write
:

.. code-block:: python

   >>> F('>', params=[E.a, E.b])

A programmer can manipulate those nested function calls with no problem, but
people with less technical background will find difficulties doing it.
``j1bz.expression`` aims to make ``b3j0f.requester`` calls more accessible. The
syntax is highly inspired from SQL, because any IT guy should have seen at
least a few SQL queries and should not be lost :

.. code-block:: python

   >>> interpret("SELECT ALL WHERE (a > b);")

The syntax is more restrictive than what native ``b3j0f.requester`` allows you
to do (main needs are covered). Thus, users are incentived to write things that
make sense.

``j1bz.expression.intepreter.interpret`` return a
``b3j0f.requester.request.crud.{create.Create,read.Read,update.Update,delete.Delete}``
serialized object (depending on the query). The object can then be processed by
any driver.

Installation
============

.. code-block:: bash

  aptitude install git virtualenv

  virtualenv venv
  source venv/bin/activate

  git clone https://github.com/b3j0f/requester

  cd requester
  python setup.py install

  pip install j1bz.expression

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
exception you have to catch when invoking interpret function as is.

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

.. code-block:: bash

  CREATE VALUES k:v;

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

.. code-block:: bash

  READ ALL;

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
``{{ PACKAGE }}/etc/j1bz/expression/grammar.bnf``. You can read this bnf
description to check for all available possibilities.

Advanced how-to
---------------

If you want to integrate ``j1bz.expression`` in your code to do more than just
``interpret()`` calls, this part is for you.

Using a custom grammar
~~~~~~~~~~~~~~~~~~~~~~

The engine powering ``j1bz.expression`` is ``grako``. Grako (for Grammar
Kompiler) take a bnf-derivated grammar file in input and generates a parser in
python code.

This package embeds a grammar file and a pre-compiled parser generated from
this grammar (``{{ PACKAGE }}/etc/j1bz/expression/grammar.bnf``).

It is possible to change this grammar and use a parser generated at runtime for
your ``interpret()`` calls :

.. code-block:: python

  >>> interpret("SELECT a;", "/PATH/TO/grammar.bnf")

**Note**: Once you've called ``interpret()`` for the first time (with or
without grammar file), the same parser used for the first time will be used
later (due to a singleton mechanic). 

Interpreter vs interpret
~~~~~~~~~~~~~~~~~~~~~~~~

``interpret()`` uses a singleton mechanic to provide a shortcut.

If you want to do more complex things, you can use the
``j1bz.expression.interpreter.Interpreter`` class.

Examples :

.. code-block:: python

  >>> i1 = Interpreter(parser=mygrakoparser, walker=mycustomwalker)
  >>> i1.interpret("SELECT a;")

  >>> i2 = Interpreter(pkwargs={'rule_name': 'condition'})
  >>> i2.interpret("(a > b)")

  >>> i3 = Interpreter(grammar_file='/PATH/TO/grammar.bnf')
  >>> i3.interpret("SELECT_ALIAS a;")

**Note**: ``grammar_file`` argument will be used only if you did not provide a
custom parser via ``parser`` argument.

Exception handling
~~~~~~~~~~~~~~~~~~

``j1bz.expression.exceptions`` currently defines 2 exceptions :

- ``ParserGenerationError`` : Raised when you provide a custom grammar in
  order to generate a   parser, but generation failed (your grammar is not
  correct !).
- ``ParseError`` : Raised when an expression given to ``interpret()`` is not
  parsable.

Some other exceptions (``IOError``, ``OSError``, ``FileNotFoundError``) can
also be raised when trying to compile a custom parser if the grammar file is
not readable, does not exist, etc.

If you're only using ``interpret()`` shortcut, you should handle all named
exceptions above.

If you're using ``Interpreter`` class, you need to handle
``ParserGenerationError`` (and file related exceptions) when you instantiate it
and ``ParseError`` when you make ``interpret()`` calls.
