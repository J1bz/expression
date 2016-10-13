#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from builtins import input

from grako.model import ModelBuilderSemantics

from j1bz.expression.walker import Walker
from j1bz.expression.parser import get_parser


def cli_interpreter(parser, walker):
    print("=== Expression CLI interpreter ===")
    print("Enter 'QUIT' to quit")
    print("")

    cmd = ''
    while True:
        try:
            cmd = input('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            break

        if cmd == 'QUIT':
            break

        model = parser.parse(cmd, rule_name='start')
        res = walker.walk(model)
        print(repr(res))


def main():
    parser = get_parser(semantics=ModelBuilderSemantics())
    walker = Walker()

    cli_interpreter(parser, walker)


if __name__ == '__main__':
    main()
