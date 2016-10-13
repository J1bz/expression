#!/usr/bin/env python
# -*- coding: utf-8 -*-

from j1bz.expression.default_parser import ExpressionParser as DefaultParser


def get_parser(*args, **kwargs):
    return DefaultParser(*args, **kwargs)
