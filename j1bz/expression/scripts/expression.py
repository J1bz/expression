#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from traceback import format_exc

from prompt_toolkit import prompt

from j1bz.expression.exceptions import ParseError
from j1bz.expression.interpreter import Interpreter


def cli_interpreter(interpreter):
    print("=== Expression CLI interpreter ===")
    print("Enter 'QUIT' to quit")
    print("")

    cmd = ''
    while True:
        try:
            cmd = prompt('> ')

        except EOFError:
            break

        except KeyboardInterrupt:
            break

        if cmd == 'QUIT':
            break

        try:
            res = interpreter.interpret(cmd)

        except ParseError as e:
            print(format_exc(e))
            continue

        print(repr(res))


def main():
    i = Interpreter()
    cli_interpreter(i)


if __name__ == '__main__':
    main()
