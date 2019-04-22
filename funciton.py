# coding=utf-8
from __future__ import unicode_literals, absolute_import

import itertools

__author__ = 'GoTop'

def peek(iterable):
    """
    返回生成器的第一个元素
    同时，因为生产器中会删除这个原始，所以将这个元素再次加入生产器中返回

    使用这个方法可以不改变生产器的情况下，获得生成器的第一个元素
    https://stackoverflow.com/a/664239/1314124
    :param iterable:
    :return:
    """
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)