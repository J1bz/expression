# -*- coding: utf-8 -*-

from sys import prefix, modules
from os.path import join, dirname
from imp import new_module
from six import exec_, raise_from
from warnings import warn

from grako.tool import genmodel
from grako.exceptions import GrakoException
from grako.codegen.python import codegen as pythoncg

from j1bz.expression.default_parser import ExpressionParser as DefaultParser
from j1bz.expression.exceptions import (
    ParserGenerationError, GrammarFallbackWarning)


def get_generated_parser(filename=None, **kwargs):
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


def get_parser(fallback=False, **kwargs):
    grammar = join(prefix, 'etc', 'j1bz', 'expression', 'grammar.bnf')
    try:
        return get_generated_parser(filename=grammar, **kwargs)

    except ParserGenerationError as e:
        if fallback:
            fallback_grammar = join(
                dirname(__file__),
                'etc', 'j1bz', 'expression', 'grammar.bnf'
            )

            warning = (
                "Compilation of {} failed. Falling back on {}.".format(
                    grammar, fallback_grammar
                )
            )
            warn(warning, GrammarFallbackWarning)

            return get_generated_parser(filename=fallback_grammar, **kwargs)

        else:
            raise e


def get_default_parser(**kwargs):
    return DefaultParser(**kwargs)
