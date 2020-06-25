# coding=utf-8
from __future__ import unicode_literals, absolute_import

import os
import re

from directory import create_dir_for_match_files_main, move_dir_to_dir, \
    move_files_to_dir_with_dir_structure
from file import rename_match_file_name_main, rename_file, strip_file_name, \
    format_date_string_2, add_date_string, get_filePath_fileName_fileExt, \
    remove_qm5_string
from string_fns import find_date_string_and_format

"""
#作者 GoTop
#时间 2017-8-19
# 将下载的足球视频文件和目录中，都会带有类似'【天下足球网www.txzqw.cc】'的等文字，太碍眼
# 本脚本可以实现以下功能：
# 1.可以在指定目录file_dir中，将所有目录和文件名中指定的字符串replace_string_list删除
# 2.可以为file_dir目录下未放入同一个目录的一场比赛的上、下半场两个视频文件，新建一个目录，然后将视频文件移动到目录中
# 3.可以根据同一目录下的两个视频文件名中的不同部分，在视频文件名中加入"上半场"或"下半场"的标识
# 4.去除文件名中多余的横杠 - ，但是不去除类似 2018-19 中的横杠
# 5.将不同的日期字符串如2019-2-28,2019.1.28,同一修改为"x月x日"这样的日期格式
# 6.对于某些没有日期的视频文件，在名称中加入执行本脚本的时间"x月x日"，以便识别
# 7.多次执行本函数不会对文件名进行重复的修改
# 8.只对指定的后缀名的文件进行改名处理

todo 对于没有日期的文件，使用该文件创建的时间来作为日期比较合理
"""
__author__ = 'GoTop'

# 执行脚本前，需要设定的内容
# 设置需要修改名称的目录
src_dir_path = r"J:\BaiduNetdiskDownload\足球"
# 设置需要移动视频文件到的目录
dst_dir_path = r"J:\Video\Download\YouTube\playlist\足球"
# file_dir = r"J:\Video\Download\YouTube\playlist\足球"
extensions = ['.mkv', '.mp4', '.ts', '.qm5']

replace_string_list = ['【天下足球网www.txzqw.cc】', '【天下足球网www.txzqw.me】',
                       '[52waha]',
                       '[Young_Andy]', '【哇哈體育】', '【哇哈体育】', '[球迷网www.qm5.cc]',
                       '【球迷网-www.qm5.cc】',
                       '【90分钟足球网】', '【劲爆足球网www.jzwzx.com】', '【劲爆足球网】',
                       '【90分钟足球网】', '魅力高清国语', '魅力音乐', '魅力足球',
                       # '18-19赛季'要在'2018-19赛季'的后面
                       '2018-19赛季', '2019-20赛季', '18-19赛季', '19-20赛季',
                       '2018-19',
                       '高清国语', 'hdtv', '720P', '1080P.',
                       '1080P',
                       '1080i',
                       '1080', 'CCTV5HD .', 'CCTV5HD.', 'CNTV',
                       'CCTV5+', 'CCTV5', '新视觉', 'PPTV', 'PP体育', '1070P',
                       '高清(50fps)',
                       # 过滤mkv这个字符串会把文件名中后缀名为.mkv的视频文件的后缀名删除
                       # 'MKV',
                       '新英', '百视通', '爱奇艺体育', '爱奇艺', '海角主', 'hdtv', 'HD', '国语',
                       'besTV', '无台标', '收藏版', '录播',
                       ]

commentator = ['詹俊', '刘越', '娄一晨', '李彦', '刘腾', '贺宇', '申方剑', '孟洪涛', '林梦鸽', '陈渤胄',
               '张力', '朱迟蕊', '刘畅', '苗霖', '董路', '鲁靖明', '张力', ]

replace_string_list = replace_string_list + commentator

# 测试使用下面设置
# src_dir_path = r"J:\Video\Download\YouTube\playlist\NA"
# dst_dir_path = "J:\Video\Download\YouTube\playlist\move"
# replace_string_list = ['PP体育', '1080P', '海角主']

if __name__ == "__main__":
    # move_same_match_files_to_directory(file_dir)

    remove_qm5_string(src_dir_path)

    # 先将有类似的两个视频文件放入同一目录中
    create_dir_for_match_files_main(src_dir_path, extensions)
    # 遍历目录，根据同一目录下，两个视频文件名中不同的部分(比如1或2，1st或2nd)，
    # 分别将视频文件命名为"上半场"+相同字段+文件后缀
    # note 重命名1st，2nd这样的字符串，能够避免以后的在视频文件名中查找日期的函数将2nd认为是日期
    rename_match_file_name_main(src_dir_path)
    # 循环遍历file_dir目录下不同层级的所有目录
    # 要设置topdown=False，这样会先遍历子目录，如果修改目录名，不会对下一个遍历造成影响
    # 否则默认先遍历根目录，如果修改目录名，会导致遍历子目录的时候目录地址改变
    for root, dirs, files in os.walk(src_dir_path, topdown=False):
        # 对file_dir目录下的文件名称进行替换
        for file_name in files:
            file_path, file_name_without_ext, extension = \
                get_filePath_fileName_fileExt(
                    file_name)
            origin_file_name = file_name

            # 如果遍历的文件的后缀不在指定的extensions视频文件列表中，则不对该文件进行处理
            if extension not in extensions:
                continue

            # 替换视频文件名中多余的字符串replace_string_list，比如网址，清晰度等
            for replace_string in replace_string_list:
                # clean_file_name(file_dir, replace_string)
                # file_name = file_name.replace(replace_string, "")
                # 不区分大小写替换
                # 参考 https://segmentfault.com/q/1010000009924890
                reg = re.compile(re.escape(replace_string), re.IGNORECASE)
                file_name = reg.sub('', file_name)
            # old_file_path = os.path.join(root, file_name)
            # 将比赛的视频文件名中不规范的日期字符串，修改为X月X日的样式
            # new_file_name = format_date_string(file_name)
            # new_file_name = format_date_string_2(file_name)
            # new_file_name = add_date_string(new_file_name)

            new_file_name = find_date_string_and_format(file_name)
            new_file_name = add_date_string(new_file_name)

            # 去除文件名中多余的空格和-
            new_file_name = strip_file_name(new_file_name)
            rename_file(root, origin_file_name, new_file_name)

            new_file_path = os.path.join(root, new_file_name)
            # # 如果文件名中有字符串被修改，则将实际的文件进行重命名
            # if new_file_path != old_file_path:
            #     os.rename(old_file_path, new_file_path)
            #     print('/n 将{}文件名替换为{}'.format(old_file_path, new_file_path))
        # 对file_dir目录下的目录的名称，该目录下的目录和文件名进行替换
        for dir_name in dirs:
            # 对于resilio sync文件的目录 .sync，不进行替换操作
            if dir_name == '.sync':
                continue
            origin_dir_name = dir_name
            for replace_string in replace_string_list:
                # dir_name = dir_name.replace(replace_string, "")
                reg = re.compile(re.escape(replace_string), re.IGNORECASE)
                dir_name = reg.sub('', dir_name)
            # 将该dir目录的名称进行替换
            # new_dir_name = format_date_string(dir_name)
            # new_dir_name = format_date_string_2(dir_name)
            # new_dir_name = add_date_string(new_dir_name)

            new_dir_name = find_date_string_and_format(dir_name)
            new_dir_name = add_date_string(new_dir_name)

            # 去除文件名中多余的空格和-
            new_dir_name = strip_file_name(new_dir_name)
            rename_file(root, origin_dir_name, new_dir_name)

    move_files_to_dir_with_dir_structure(src_dir_path, dst_dir_path,
                                         extensions)
