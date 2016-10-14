Description
===========

Expression is a Domain Specific Language (DSL) designed to express CRUD queries for Crudity (https://github.com/b3j0f/requester/).

In other words, you can write Crudity Expressions.

Installation
============

.. code:: bash
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

Examples
========

TODO
