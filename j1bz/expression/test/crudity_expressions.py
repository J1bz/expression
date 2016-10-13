#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main, TestCase

from grako.model import ModelBuilderSemantics

from j1bz.expression.walker import Walker
from j1bz.expression.parser import get_parser


class CrudityExpressionsTest(TestCase):
    def setUp(self):
        self.parser = get_parser(semantics=ModelBuilderSemantics())
        self.walker = Walker()

    def test_create(self):
        creates = [
            ('SELECT s;', 'READ s'),
            ('SELECT s WHERE w;', 'READ s where (w)'),
        ]

        for create, expected in creates:
            model = self.parser.parse(create)
            res = self.walker.walk(model)

            self.assertEqual(repr(res), expected)

    def test_read(self):
        reads = [
        ]

        for read, expected in reads:
            model = self.parser.parse(read)
            res = self.walker.walk(model)

            self.assertEqual(res, expected)

    def test_update(self):
        updates = [
        ]

        for update, expected in updates:
            model = self.parser.parse(update)
            res = self.walker.walk(model)

            self.assertEqual(res, expected)

    def test_delete(self):
        deletes = [
        ]

        for delete, expected in deletes:
            model = self.parser.parse(delete)
            res = self.walker.walk(model)

            self.assertEqual(res, expected)


if __name__ == '__main__':
    main()
