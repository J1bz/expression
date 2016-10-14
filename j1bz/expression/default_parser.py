#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__all__ = [
    'ExpressionParser',
    'ExpressionSemantics',
    'main'
]

KEYWORDS = set([
    'AND',
    'ASC',
    'BY',
    'CREATE',
    'DELETE',
    'DESC',
    'FALSE',
    'GROUP',
    'IN',
    'INSERT',
    'INTO',
    'LIKE',
    'LIMIT',
    'NIN',
    'NULL',
    'OR',
    'ORDER',
    'READ',
    'SELECT',
    'TRUE',
    'UPDATE',
    'VALUES',
    'WHERE',
    'WITH',
])


class ExpressionBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(ExpressionBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class ExpressionParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=ExpressionBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(ExpressionParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken('true')
    def _true_(self):
        self._token('TRUE')

    @graken('false')
    def _false_(self):
        self._token('FALSE')

    @graken('digits')
    def _digits_(self):
        self._pattern(r'[0-9]+')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('characters')
    def _characters_(self):
        self._pattern(r'\w*')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _string_(self):
        with self._choice():
            with self._option():
                self._token('"')
                self._characters_()
                self.name_last_node('value')
                self._token('"')
            with self._option():
                self._token("'")
                self._characters_()
                self.name_last_node('value')
                self._token("'")
            self._error('no available options')
        self.ast._define(
            ['value'],
            []
        )

    @graken('sign')
    def _sign_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('+')
                with self._option():
                    self._token('-')
                self._error('expecting one of: + -')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('integer')
    def _integer_(self):
        with self._optional():
            self._sign_()
            self.name_last_node('sign')
        self._digits_()
        self.name_last_node('value')
        self.ast._define(
            ['sign', 'value'],
            []
        )

    @graken('floating')
    def _floating_(self):
        with self._optional():
            self._sign_()
            self.name_last_node('sign')
        self._digits_()
        self.name_last_node('intpart')
        self._token('.')
        self._digits_()
        self.name_last_node('floatpart')
        self.ast._define(
            ['floatpart', 'intpart', 'sign'],
            []
        )

    @graken('forward_value')
    def _boolean_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._true_()
                with self._option():
                    self._false_()
                self._error('no available options')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('none')
    def _none_(self):
        self._token('NULL')

    @graken('name')
    def _name_(self):
        with self._group():
            self._pattern(r'[_a-zA-Z][_a-zA-Z0-9]*(\.[_a-zA-Z][_a-zA-Z0-9]*)*')
        self.name_last_node('value')
        self._check_name()
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _as_(self):
        self._token('AS')
        self._name_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('expression')
    def _expression_(self):
        self._name_()
        self.name_last_node('name')
        with self._optional():
            self._as_()
            self.name_last_node('as_')
        self.ast._define(
            ['as_', 'name'],
            []
        )

    @graken('function')
    def _function_(self):
        self._name_()
        self.name_last_node('f')
        self._token('(')

        def sep2():
            self._token(',')

        def block2():
            self._value_()
        self._closure(block2, sep=sep2)
        self.name_last_node('args')
        self._token(')')
        with self._optional():
            self._as_()
            self.name_last_node('as_')
        self.ast._define(
            ['args', 'as_', 'f'],
            []
        )

    @graken('forward_value')
    def _value_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._function_()
                with self._option():
                    self._expression_()
                with self._option():
                    self._string_()
                with self._option():
                    self._floating_()
                with self._option():
                    self._integer_()
                with self._option():
                    self._boolean_()
                with self._option():
                    self._none_()
                with self._option():
                    self._crud_()
                self._error('no available options')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _identifier_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._function_()
                with self._option():
                    self._expression_()
                self._error('no available options')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('condop')
    def _condop_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('AND')
                with self._option():
                    self._token('OR')
                with self._option():
                    self._token('<=')
                with self._option():
                    self._token('<')
                with self._option():
                    self._token('=')
                with self._option():
                    self._token('!=')
                with self._option():
                    self._token('>=')
                with self._option():
                    self._token('>')
                with self._option():
                    self._token('IN')
                with self._option():
                    self._token('NIN')
                with self._option():
                    self._token('LIKE')
                self._error('expecting one of: != < <= = > >= AND IN LIKE NIN OR')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('condition')
    def _condition_(self):
        with self._choice():
            with self._option():
                self._token('(')
                self._condition_()
                self.name_last_node('left')
                self._condop_()
                self.name_last_node('condop')
                self._condition_()
                self.name_last_node('right')
                self._token(')')
            with self._option():
                self._token('(')
                self._value_()
                self.name_last_node('left')
                self._token(')')
            with self._option():
                self._value_()
                self.name_last_node('left')
            self._error('no available options')
        self.ast._define(
            ['condop', 'left', 'right'],
            []
        )

    @graken('kv')
    def _kv_(self):
        self._identifier_()
        self.name_last_node('key')
        self._token(':')
        self._value_()
        self.name_last_node('value')
        self.ast._define(
            ['key', 'value'],
            []
        )

    @graken('kvs')
    def _kvs_(self):

        def sep1():
            self._token(',')

        def block1():
            self._kv_()
        self._positive_closure(block1, sep=sep1)
        self.name_last_node('kvs')
        self.ast._define(
            ['kvs'],
            []
        )

    @graken('kv')
    def _strkey_value_(self):
        self._string_()
        self.name_last_node('key')
        self._token(':')
        self._value_()
        self.name_last_node('value')
        self.ast._define(
            ['key', 'value'],
            []
        )

    @graken('kvs')
    def _strkeys_values_(self):

        def sep1():
            self._token(',')

        def block1():
            self._strkey_value_()
        self._positive_closure(block1, sep=sep1)
        self.name_last_node('kvs')
        self.ast._define(
            ['kvs'],
            []
        )

    @graken('forward_value')
    def _where_(self):
        self._token('WHERE')
        self._condition_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('groupby')
    def _groupby_(self):
        self._token('GROUP BY')

        def sep1():
            self._token(',')

        def block1():
            self._identifier_()
            self.name_last_node('name')
        self._positive_closure(block1, sep=sep1)
        self.name_last_node('values')
        self.ast._define(
            ['name', 'values'],
            []
        )

    @graken('sorter')
    def _sorter_(self):
        self._identifier_()
        self.name_last_node('name')
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('ASC')
                with self._option():
                    self._token('DESC')
                self._error('expecting one of: ASC DESC')
        self.name_last_node('sortmod')
        self.ast._define(
            ['name', 'sortmod'],
            []
        )

    @graken('orderby')
    def _orderby_(self):
        self._token('ORDER BY')

        def sep1():
            self._token(',')

        def block1():
            self._sorter_()
            self.name_last_node('sorter')
        self._positive_closure(block1, sep=sep1)
        self.name_last_node('values')
        self.ast._define(
            ['sorter', 'values'],
            []
        )

    @graken('forward_value')
    def _limit_(self):
        self._token('LIMIT')
        self._integer_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('with')
    def _with_(self):
        self._token('WITH')
        self._strkeys_values_()
        self.name_last_node('dparams')
        self.ast._define(
            ['dparams'],
            []
        )

    @graken()
    def _create_start_(self):
        with self._choice():
            with self._option():
                self._token('INSERT')
            with self._option():
                self._token('CREATE')
            self._error('expecting one of: CREATE INSERT')

    @graken('create')
    def _create_(self):
        with self._optional():
            self._token('INTO')
            self._identifier_()
            self.name_last_node('name')
        self._token('VALUES')
        self._kvs_()
        self.name_last_node('fields')
        with self._optional():
            self._with_()
            self.name_last_node('with_')
        self.ast._define(
            ['fields', 'name', 'with_'],
            []
        )

    @graken('forward_value')
    def _create_brackets_(self):
        self._create_start_()
        self._token('(')
        self._create_()
        self.name_last_node('value')
        self._token(')')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _create_nobrackets_(self):
        self._create_start_()
        self._create_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken()
    def _read_start_(self):
        with self._choice():
            with self._option():
                self._token('READ')
            with self._option():
                self._token('SELECT')
            self._error('expecting one of: READ SELECT')

    @graken('read')
    def _read_(self):

        def sep1():
            self._token(',')

        def block1():
            self._identifier_()
        self._positive_closure(block1, sep=sep1)
        self.name_last_node('names')
        with self._optional():
            self._where_()
            self.name_last_node('where')
        with self._optional():
            self._groupby_()
            self.name_last_node('groupby')
        with self._optional():
            self._orderby_()
            self.name_last_node('orderby')
        with self._optional():
            self._limit_()
            self.name_last_node('limit')
        with self._optional():
            self._with_()
            self.name_last_node('with_')
        self.ast._define(
            ['groupby', 'limit', 'names', 'orderby', 'where', 'with_'],
            []
        )

    @graken('forward_value')
    def _read_brackets_(self):
        self._read_start_()
        self._token('(')
        self._read_()
        self.name_last_node('value')
        self._token(')')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _read_nobrackets_(self):
        self._read_start_()
        self._read_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken()
    def _update_start_(self):
        self._token('UPDATE')

    @graken('update')
    def _update_(self):
        with self._optional():
            self._token('INTO')
            self._identifier_()
            self.name_last_node('name')
        self._token('VALUES')
        self._kvs_()
        self.name_last_node('fields')
        with self._optional():
            self._where_()
            self.name_last_node('where')
        with self._optional():
            self._with_()
            self.name_last_node('with_')
        self.ast._define(
            ['fields', 'name', 'where', 'with_'],
            []
        )

    @graken('forward_value')
    def _update_brackets_(self):
        self._update_start_()
        self._token('(')
        self._update_()
        self.name_last_node('value')
        self._token(')')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _update_nobrackets_(self):
        self._update_start_()
        self._update_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken()
    def _delete_start_(self):
        self._token('DELETE')

    @graken('delete')
    def _delete_(self):

        def sep1():
            self._token(',')

        def block1():
            self._identifier_()
        self._positive_closure(block1, sep=sep1)
        self.name_last_node('names')
        with self._optional():
            self._where_()
            self.name_last_node('where')
        with self._optional():
            self._with_()
            self.name_last_node('with_')
        self.ast._define(
            ['names', 'where', 'with_'],
            []
        )

    @graken('forward_value')
    def _delete_brackets_(self):
        self._delete_start_()
        self._token('(')
        self._delete_()
        self.name_last_node('value')
        self._token(')')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _delete_nobrackets_(self):
        self._delete_start_()
        self._delete_()
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _crudop_brackets_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._create_brackets_()
                with self._option():
                    self._read_brackets_()
                with self._option():
                    self._update_brackets_()
                with self._option():
                    self._delete_brackets_()
                self._error('no available options')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('forward_value')
    def _crudop_nobrackets_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._create_nobrackets_()
                with self._option():
                    self._read_nobrackets_()
                with self._option():
                    self._update_nobrackets_()
                with self._option():
                    self._delete_nobrackets_()
                self._error('no available options')
        self.name_last_node('value')
        self.ast._define(
            ['value'],
            []
        )

    @graken('crud')
    def _crud_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._crudop_nobrackets_()
                    self.name_last_node('crudop')
                with self._option():
                    self._crudop_brackets_()
                    self.name_last_node('crudop')
                    with self._optional():
                        self._as_()
                        self.name_last_node('as_')
                self._error('no available options')
        self._token(';')
        self.ast._define(
            ['as_', 'crudop'],
            []
        )

    @graken('forward_value')
    def _request_(self):
        self._value_()
        self.name_last_node('value')
        self._check_eof()
        self.ast._define(
            ['value'],
            []
        )

    @graken()
    def _start_(self):
        self._request_()
        self.name_last_node('request')
        self.ast._define(
            ['request'],
            []
        )


class ExpressionSemantics(object):
    def true(self, ast):
        return ast

    def false(self, ast):
        return ast

    def digits(self, ast):
        return ast

    def characters(self, ast):
        return ast

    def string(self, ast):
        return ast

    def sign(self, ast):
        return ast

    def integer(self, ast):
        return ast

    def floating(self, ast):
        return ast

    def boolean(self, ast):
        return ast

    def none(self, ast):
        return ast

    def name(self, ast):
        return ast

    def as_(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def function(self, ast):
        return ast

    def value(self, ast):
        return ast

    def identifier(self, ast):
        return ast

    def condop(self, ast):
        return ast

    def condition(self, ast):
        return ast

    def kv(self, ast):
        return ast

    def kvs(self, ast):
        return ast

    def strkey_value(self, ast):
        return ast

    def strkeys_values(self, ast):
        return ast

    def where(self, ast):
        return ast

    def groupby(self, ast):
        return ast

    def sorter(self, ast):
        return ast

    def orderby(self, ast):
        return ast

    def limit(self, ast):
        return ast

    def with_(self, ast):
        return ast

    def create_start(self, ast):
        return ast

    def create(self, ast):
        return ast

    def create_brackets(self, ast):
        return ast

    def create_nobrackets(self, ast):
        return ast

    def read_start(self, ast):
        return ast

    def read(self, ast):
        return ast

    def read_brackets(self, ast):
        return ast

    def read_nobrackets(self, ast):
        return ast

    def update_start(self, ast):
        return ast

    def update(self, ast):
        return ast

    def update_brackets(self, ast):
        return ast

    def update_nobrackets(self, ast):
        return ast

    def delete_start(self, ast):
        return ast

    def delete(self, ast):
        return ast

    def delete_brackets(self, ast):
        return ast

    def delete_nobrackets(self, ast):
        return ast

    def crudop_brackets(self, ast):
        return ast

    def crudop_nobrackets(self, ast):
        return ast

    def crud(self, ast):
        return ast

    def request(self, ast):
        return ast

    def start(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = ExpressionParser(parseinfo=False)
    return parser.parse(text, startrule, filename=filename, **kwargs)

if __name__ == '__main__':
    import json
    ast = generic_main(main, ExpressionParser, name='Expression')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

