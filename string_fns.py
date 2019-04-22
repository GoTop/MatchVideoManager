# coding=utf-8
from __future__ import unicode_literals, absolute_import

import re
import time

__author__ = 'GoTop'


def find_date_string_and_format(origin_str):
    """
    查找origin_str字符串中的日期格式的部分，将其替换成x月x日的形式并返回

    :param origin_str:
    :return:
    """
    # 要先匹配长的模式，再匹配断的模式
    # 匹配"2019年1月20日","2019年01月08日"这样的日期
    search_obj = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', origin_str)
    if search_obj:
        match_date_str = search_obj.group()
        convert_date_str = '{}月{}日'.format(int(search_obj.group(2)),
                                           int(search_obj.group(3)))
        format_date_str = origin_str.replace(match_date_str, convert_date_str)
        return format_date_str
    # 匹配"1月20日","01月05日"这样的日期
    search_obj = re.search(r'(\d{1,2})月(\d{1,2})日', origin_str)
    if search_obj:
        match_date_str = search_obj.group()
        convert_date_str = '{}月{}日'.format(int(search_obj.group(1)),
                                           int(search_obj.group(2)))
        format_date_str = origin_str.replace(match_date_str, convert_date_str)
        return format_date_str
    # 匹配"2019.2.28","2019.02.8"这样的日期
    search_obj = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', origin_str)

    if search_obj:
        match_date_str = search_obj.group()
        convert_date_str = '{}月{}日'.format(int(search_obj.group(2)),
                                           int(search_obj.group(3)))
        format_date_str = origin_str.replace(match_date_str, convert_date_str)
        return format_date_str
    # 匹配"2019-02-09","2019-02-12"这样的日期
    search_obj = re.search(r'(\d{4})\-(\d{1,2})\-(\d{1,2})', origin_str)
    if search_obj:
        match_date_str = search_obj.group()
        convert_date_str = '{}月{}日'.format(int(search_obj.group(2)),
                                           int(search_obj.group(3)))
        format_date_str = origin_str.replace(match_date_str, convert_date_str)
        return format_date_str
    return origin_str
