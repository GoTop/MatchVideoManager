# coding=utf-8
from __future__ import unicode_literals, absolute_import

import datefinder

from directory import move_files_to_dir_with_dir_structure
from file import strip_file_name, format_date_string_2
from string_fns import find_date_string_and_format

__author__ = 'GoTop'

# file_name = "下半场 3月9日 -1月26日 足总杯第4轮 曼城VS伯恩利 .mkv"
# replace_string_list = ['【天下足球网www.txzqw.cc】', '【天下足球网www.txzqw.me】',
#                        '17-18赛季', '2018-19赛季', '[52waha]',
#                        '[Young_Andy]', '【哇哈體育】', '[球迷网www.qm5.cc]', '【90分钟足球网】',
#                        '【90分钟足球网】', '高清国语', 'hdtv', '720P', '1080P', '1080i',
#                        '1080',
#                        'CCTV5+', 'CCTV5', '新视觉', 'PPTV', 'PP体育', '1070P',
#                        '新英', '百视通', '海角主', 'hdtv', 'HD', '国语']
#
# # print(strip_file_name(file_name))
#
# # for replace_string in replace_string_list:
# #     # clean_file_name(file_dir, replace_string)
# #     file_name = file_name.replace(replace_string, "")
# #
# # print(file_name)
#
# origin_str = "2019年01月26日 【天下足球网www.txzqw.cc】足总杯第4轮 曼城VS伯恩利 PPTV.mkv"
# origin_str = "2019.2.28 英超 水晶宫VS曼联 PP体育 1080P 海角主"
# format_date_str = find_date_string_and_format(origin_str)
#
# print(format_date_string_2(format_date_str))

src_dir_path = r"J:\Video\Download\YouTube\playlist\NA"
dst_dir_path = "J:\Video\Download\YouTube\playlist\move"
extensions = ['.mkv', '.mp4', '.ts', ]
move_files_to_dir_with_dir_structure(src_dir_path, dst_dir_path, extensions)
