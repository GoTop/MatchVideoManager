# coding=utf-8
from __future__ import unicode_literals, absolute_import

import os

from clean_file_name import format_date_string

__author__ = 'GoTop'

def clean_file_name(file_dir, replace_string):
    """
    分别遍历file_dir目录下所有的目录和文件，如果目录或者文件名中包含replace_string字符串的，
    将目录或者文件名中的该字符串去除
    :param file_dir:
    :param replace_string:
    :return:
    """
    # 循环遍历file_dir目录下不同层级的所有目录
    # 要设置topdown=False，这样会先遍历子目录，如果修改目录名，不会对下一个遍历造成影响
    # 否则默认先遍历根目录，如果修改目录名，会导致遍历子目录的时候目录地址改变
    for root, dirs, files in os.walk(file_dir, topdown=False):
        # 对file_dir目录下的文件名称进行替换
        for file_name in files:
            old_file = os.path.join(root, file_name)

            # 将比赛的视频文件名中不规范的日期字符串，修改为X月X日的样式
            new_file = format_date_string(file_name)

            # new_file = add_date_string_to_filename(filename_fomate_date)

            new_file = new_file.replace(replace_string, "")

            new_file = os.path.join(root, new_file)
            if new_file != old_file:
                os.rename(old_file, new_file)
                print('将{old_file}文件名替换为{new_file}'.format(old_file=old_file,
                                                              new_file=new_file))
        # 对file_dir目录下的目录的名称，该目录下的目录和文件名进行替换
        for dir_name in dirs:
            # 对于resilio sync文件的目录 .sync，不进行替换操作
            if dir_name == '.sync':
                continue
            old_dir = os.path.join(root, dir_name)
            # 将该dir目录的名称进行替换
            new_dir = format_date_string(dir_name)

            new_dir = new_dir.replace(replace_string, "")

            new_dir = os.path.join(root, new_dir)
            if new_dir != old_dir:
                try:
                    # 对文件名进行修改
                    os.rename(old_dir, new_dir)
                    print('将{old_dir}目录名替换为{new_dir}'.format(old_dir=old_dir,
                                                               new_dir=new_dir))
                except FileExistsError as e:
                    print(e)
                    print("错误,需要改名的文件{}已存在,跳过该目录{}").format(old_dir, new_dir)

                    # 递归调用原函数，对该dir目录下的文件和目录名称进行递归替换
                    # 因为dir已经被改名为new_dir，所以要传入new_dir的值
                    clean_file_name(new_dir, replace_string)