# -*- coding: utf-8 -*-

from sys import prefix, modules
from os.path import join
from imp import new_module
from six import exec_, raise_from

from grako.tool import genmodel
from grako.exceptions import GrakoException
from grako.codegen.python import codegen as pythoncg

from j1bz.expression.default_parser import ExpressionParser as DefaultParser
from j1bz.expression.exceptions import ParserGenerationError


def get_generated_parser(**kwargs):
    filename = join(prefix, 'etc', 'j1bz', 'expression', 'grammar.bnf')
    with open(filename) as f:
        grammar = f.read()

        try:
            model = genmodel('Expression', grammar, filename=filename)
            code = pythoncg(model)

        except GrakoException as e:
            err = ("Error trying to generate grako parser. Is your grammar {} "
                   "correct ?".format(filename))
            raise_from(ParserGenerationError(err), e)

    dynamic_name = ('j1bz.expression.dynamic_parser')
    module = new_module(dynamic_name)
    exec_(code, module.__dict__)
    modules[dynamic_name] = module

    from j1bz.expression.dynamic_parser import ExpressionParser

    return ExpressionParser(**kwargs)


def get_parser(default_fallback=False, **kwargs):
    try:
        return get_generated_parser(**kwargs)

    except ParserGenerationError as e:
        if default_fallback:
            return DefaultParser(**kwargs)

        else:
            raise e
