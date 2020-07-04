# coding=utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import os
import re
from difflib import SequenceMatcher
import datefinder

from funciton import peek

__author__ = 'GoTop'


def get_filePath_fileName_fileExt(file):
    """
    获取文件路径、文件名、后缀名

    参考 https://blog.csdn.net/insisted_search/article/details/60156283
    :param filename:
    :return:
    """
    (file_path, temp_file_name) = os.path.split(file)
    (file_name, extension) = os.path.splitext(temp_file_name)
    return file_path, file_name, extension


def rename_file(root, old_file_name, new_file_name):
    """
    将root目录下的文件或者文件夹的名字从old_file_name改名为new_file_name

    :param root:
    :param old_file_name:
    :param new_file_name:
    :return:
    """
    # 如果文件名中有字符串被修改，则将实际的文件进行重命名
    if old_file_name != new_file_name:
        old_file_path = os.path.join(root, old_file_name)
        new_file_path = os.path.join(root, new_file_name)
        try:
            # 对文件或者目录名进行修改
            os.rename(old_file_path, new_file_path)
            if os.path.isfile(new_file_path):
                print('将"{}"文件名替换为"{}"'.format(old_file_path, new_file_path))

            if os.path.isdir(new_file_path):
                print('将"{}"目录名替换为"{}"'.format(old_file_path, new_file_path))
        except FileExistsError as e:
            print(e)
            print(("错误,需要改名的文件或者目录'{}'已存在,跳过目录'{}'的创建").format(old_file_path,
                                                               new_file_path))


def format_date_string_2(string_with_date):
    """
    查找字符串string_with_dates中的日期字样的字符串，将其提取出来，改为指定的日期格式(x
    月x日)后，替换回string_with_dates字符串中，并将替换后的字符串返回
    todo  datefinder.find_dates()会将'2nd'识别成日期，转化成'2月2日'
    :param string_with_date:
    :return:
    """
    # 要设置strict=False，否则在win7系统的python3.6下执行该脚本是，会将
    matches = datefinder.find_dates(string_with_date, True)
    res = peek(matches)
    # 如果查找到有日期(2019-2-27之类)的字符串
    if res is None:
        pass
    else:
        first, matches = res
        # 如果文件名或目录中有日期(2019-2-27之类)的字符串(除了x月x日这样的)，则
        for datetime_obj, match_date_string in matches:
            print(
                "查找到{}中有日期字符串:{}".format(string_with_date, match_date_string))
            # 使用strftime()来生成想要的日期字符串时，月份和日期的数字前可能会有前导0，可以用这个方法解决
            # https://stackoverflow.com/a/16097385/1314124
            rename_date_string = '{dt.month}月{dt.day}日'.format(dt=datetime_obj)
            print(rename_date_string)
            if rename_date_string == match_date_string:
                # 如果在string_with_dates字符串中查找到的日期字符串，修改日期的时候和tring_with_dates一样
                # 则不需要进行替换
                continue
            string_with_date = string_with_date.replace(match_date_string,
                                                        rename_date_string)

    return string_with_date

def remove_qm5_string(src_dir_path):
    """
    qm5.cc网站上传到百度云的视频文件会以'.qm5'作为视频文件的后缀，比如:
    【球迷网-www.qm5.cc】2020年6月21日 英超第30轮 阿斯顿维拉vs切尔西 PPTV国语-娄一晨+刘越+朱迟蕊 1080P.mkv.qm5

    本函数会将文件名结尾处的'.qm5'字符串删除，但是不会删除其他位置的'.qm5'字符串
    :param file_name:
    :return:
    """
    for root, dirs, files in os.walk(src_dir_path, topdown=False):
        # 对file_dir目录下的文件名称进行替换
        for file_name in files:
            file_path, file_name_without_ext, extension = \
                get_filePath_fileName_fileExt(
                    file_name)
            origin_file_name = file_name
            # 将 + 号替换成空格
            new_file_name = re.sub("\.qm5$", "", file_name)
            rename_file(root, origin_file_name, new_file_name)

def add_date_string(string_with_date):
    """
    为没有"x月x日"日期的文件或目录名，增加当前的日期

    :param string_with_date:
    :return:
    """
    # datefinder()无法判断"x月x日"这样格式的日期，所以只能用正则来判断
    m = re.search(r'\d{1,2}月\d{1,2}日', string_with_date)
    # 如果文件名中没有"x月x日"这样格式的日期的字样，说明未处理过
    if not m:
        datetime_obj = datetime.datetime.now()
        rename_date_string = '{dt.month}月{dt.day}日'.format(dt=datetime_obj)

        # 如果文件名string_with_date中有'上半场', '下半场'的字样，说明是比赛视频文件
        # 将现在文件名中的'上半场', '下半场'后面加上现在的日期"x月x日"
        if string_with_date.find('上半场') != -1 or string_with_date.find(
                '下半场') != -1:
            # note 海角主的1080p的视频，上下半场的命名只有'上半场', '下半场',没有日期，
            # 如果再后面加入当前日期则日期不正确，所以先取消在视频上加入日期的功能
            # 只要目录有日期就可以了
            pass
            # match_seq_string_list = ['上半场', '下半场']
            # for match_seq_string in match_seq_string_list:
            #     string_with_date = string_with_date.replace(match_seq_string,
            #                                                 match_seq_string + ' ' +
            #                                                 rename_date_string)
        else:
            # 如果文件名中没有 '上半场', '下半场'的字符串，则是目录或者整场比赛一个视频
            # 在文件名前面加入当前的日期"x月x日"
            string_with_date = rename_date_string + ' ' + string_with_date
    return string_with_date


def rename_match_file_name(file_dir, file_list):
    """
    获取file_dir目录下的file_list两个足球比赛上、下半场的视频文件(只有文件名)中相同字段,
    然后根据这两个视频文件名中不同的部分(1或2，1st或2nd)，分别将视频文件命名为"上半场"+相同字段+文件后缀

    只处理file_dir目录中只有2个视频文件(file_list的元素=2)的情况，
    1个，或者3个以上的视频文件都不处理
    :param file_dir:
    :param file_list:
    :return:
    """
    # 如果目录下的文件有2个，说明有上、下半场两个视频文件
    if len(file_list) == 2:
        # 获取视频的文件名，不带后缀
        file_name_a = os.path.splitext(file_list[0])[0]
        file_name_b = os.path.splitext(file_list[1])[0]
        file_name_list = [file_name_a, file_name_b]
        # 视频文件的后缀(带.),比如.mkv
        file_extend = os.path.splitext(file_list[0])[1]
        # https://stackoverflow.com/a/39404777/1314124
        match = SequenceMatcher(None, file_name_a,
                                file_name_b).find_longest_match(
            0, len(file_name_a), 0, len(file_name_b))
        match_string = file_name_a[match.a: match.a + match.size]
        for file_name in file_name_list:
            # 将视频文件的名称file_name去除相同部分的字符match_string,再前后删除空白符号
            # 注意,这里不能对match_string进行strip(),因为如果match_string前后包含空格的话,
            # 通过替换match_string.strip()得到的diff_string前后就会有空格
            diff_string = file_name.replace(match_string, '').strip()
            """
            处理文件名为:
            12月10日 法甲第24轮 巴黎圣日耳曼VS波尔多 PPTV.mkv
            22月10日 法甲第24轮 巴黎圣日耳曼VS波尔多 PPTV.mkv
            的情况

            处理文件名为:
            2019-02-09 英超 富勒姆vs曼联 hdtv 1st.mkv
            2019-02-09 英超 富勒姆vs曼联 hdtv 2nd.mkv
            的情况
            """
            # .lower()转化成小写再比较,防止无法匹配1ST的情况
            # 处理diff_string = 上半场的情况,可以将原本位于文件名尾部的"上半场"在文件名钱标注出来
            if diff_string == "1" or diff_string.lower() == "1st" or diff_string == "上半场":
                new_file_name_prefix = "1-上半场 "
            elif diff_string == "2" or diff_string.lower() == "2nd" \
                    or diff_string == "下半场":
                new_file_name_prefix = "2-下半场 "
            else:
                continue

            old_file = os.path.join(file_dir, file_name + file_extend)
            # 注意:match_string只能在这里才使用.strip()对前后删除空白符
            # 在前面diff_string的时候不能对match_string使用strip()
            new_file = os.path.join(file_dir,
                                    new_file_name_prefix +
                                    match_string.strip() + file_extend)
            if new_file != old_file:
                try:
                    os.rename(old_file, new_file)
                    print('成功将{}文件名替换为{}'.format(
                        old_file, new_file))
                except FileExistsError as e:
                    print(e)
                    print(("错误,需要改名的文件{}已存在,跳过该目录").format(
                        old_file))


def strip_file_name(file_path):
    """
    先将前后有空格的-替换成空格，但是不替换前后不是空格的-，比如2018-19，
    删除文件名中-,+,(,)
    再将连续的空格替换成一个空格

    再去除file_name前后的空格' '，这一步一定要放在后面
    :param file_name:
    :return:
    """

    file_path, file_name, extension = get_filePath_fileName_fileExt(file_path)
    # 将 + 号替换成空格
    file_name = re.sub("\+", " ", file_name)

    file_name = re.sub("\(|\)|\（ |\）", " ", file_name)
    # 将前后有空格的-替换成空格，不替换前后不是空格的-，比如2018-19，
    file_name = re.sub(r"(\s+-+\s+|\s+-+|-+\s+)", " ", file_name)
    # 将连续的空格替换成一个空格
    file_name = re.sub(r'\s+', ' ', file_name)
    # 再去除file_name前后的空格' '
    file_name = file_name.strip()

    return os.path.join(file_path, file_name + extension)


def rename_match_file_name_main(file_dir):
    """
    整合型函数
    遍历file_dir目录下的各个目录，查找所有目录中有2个视频文件的，
    获取这两个足球比赛上、下半场的视频文件(只有文件名)中相同字段,
    然后根据视频文件名中不同的部分(1或2，1st或2nd)，分别将视频文件命名为"上半场"+相同字段+文件后缀
    :param file_dir:
    :return:
    """
    for root, dirs, files in os.walk(file_dir):
        # 当遍历非file_dir目录(也就是file_dir目录的下一级目录(单场比赛的目录)的时候)
        # 将目录下的文件中的1，2或者1st,2nd修改为上半场，下半场
        rename_match_file_name(root, files)
