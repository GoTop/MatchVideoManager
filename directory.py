# coding=utf-8
from __future__ import unicode_literals, absolute_import

import os
import shutil
from difflib import SequenceMatcher, get_close_matches

from file import get_filePath_fileName_fileExt

__author__ = 'GoTop'


def create_dir_for_files(file_dir, file_list):
    """
    为file_dir目录下file_list中两个视频文件(只有文件名)，从这两个文件的文件名中提取相同的字段
    用这个字段作为目录名，在file_dir目录下新建一个目录
    :param file_dir:
    :param file_list:
    :return:
    """
    if len(file_list) == 2:
        # 获取视频的文件名，不带后缀
        file_name_a = os.path.splitext(file_list[0])[0]
        file_name_b = os.path.splitext(file_list[1])[0]
        # https://stackoverflow.com/a/39404777/1314124
        match = SequenceMatcher(None, file_name_a,
                                file_name_b).find_longest_match(
            0, len(file_name_a), 0, len(file_name_b))
        match_string = file_name_a[match.a: match.a + match.size]
        match_string = match_string.strip()
        dir_path = os.path.join(file_dir, match_string)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return dir_path
    else:
        return False


def move_same_match_files_to_directory(file_dir):
    """
    对于file_dir目录下所有 文件名第一个字不同，但其他都相同的两个文件，
    比如:
    11月26日 足总杯第4轮 曼城VS伯恩利 PPTV.mkv
    21月26日 足总杯第4轮 曼城VS伯恩利 PPTV.mkv
    创建一个名为"1月26日 足总杯第4轮 曼城VS伯恩利 PPTV"的目录，并将这两个文件移动到该目录下
    note 停用，改用更先进的方法来智能识别一场比赛的上下半场视频文件
    :param file_dir:
    :return:
    """
    # 循环遍历file_dir目录下不同层级的所有目录
    for root, dirs, files in os.walk(file_dir):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
        # ".sync"目录是Rsilio软件用来保存同步记录的，本函数不对该文件进行处理，跳过
        if root == os.path.join(file_dir, ".sync"):
            continue
        # 对file_dir目录下的文件名称进行替换
        delete_first_letter_file_name_list = []
        for file in files:
            (filename, extension) = os.path.splitext(file)
            # 如果在root目录的地址中查找到filename字符串，说明该视频文件已经放置到指定目录，
            # 不需要进行以下的操作了
            r = root.find(filename[1:])
            if root.find(filename[1:]) != -1:
                # find()如果查找不到字符串会返回-1
                continue

            # 保存当前遍历的目录下的所有文件，去除视频文件名的第一个字符后的字符串
            # 比如:去除“110月2日 17-18赛季西甲第7轮 皇家马德里VS西班牙人 PPTV高清国语.mkv”
            # 中的第一个字符1
            delete_first_letter_file_name_list.append(filename[1:])

        if delete_first_letter_file_name_list != []:
            # 当该目录下有视频文件时，查找delete_first_letter_file_name_list中的重复的文件名称
            import collections
            dup_file_name_list = [item for item, count in
                                  collections.Counter(
                                      delete_first_letter_file_name_list).items()
                                  if count > 1]
        else:
            # 当该目录下没有视频文件时，delete_first_letter_file_name_list=[]
            # 此时应进入下一个目录进行遍历
            continue

        # 如果找到重复的文件名，执行创建目录，移动文件的操作
        if dup_file_name_list:
            # 查找重复的比赛名称在list中的index
            for dup_file_name in dup_file_name_list:
                # 为重复的视频文件创建目录
                dup_file_directory = os.path.join(root, dup_file_name)
                if not os.path.exists(dup_file_directory):
                    os.mkdir(dup_file_directory)

                # 查找重复的视频名称在dup_file_name_list中的所有下标
                # https://stackoverflow.com/a/9542768
                dup_file_name_index_list = [i for i, file_name in enumerate(
                    delete_first_letter_file_name_list) if file_name ==
                                            dup_file_name]

                # 将重复的文件移动到同一个目录中
                for dup_file_name_index in dup_file_name_index_list:
                    origin_file = os.path.join(root, files[dup_file_name_index])
                    new_file = os.path.join(dup_file_directory,
                                            files[dup_file_name_index])
                    shutil.move(origin_file, new_file)


def move_files_to_dir(origin_dir, dest_dir, file_list):
    """
    将file_list列表中的文件(只有文件名称)(位于origin_dir目录下)，移动到dest_dir目录
    :param origin_dir:
    :param dest_dir:
    :param file_list:
    :return:
    """
    for file_name in file_list:
        origin_file_path = os.path.join(origin_dir, file_name)
        dest_file_path = os.path.join(dest_dir, file_name)
        shutil.move(origin_file_path, dest_file_path)


def move_dir_to_dir(src_dir_path, dst_dir_path):
    if not os.path.exists(src_dir_path):
        print("源文件夹不存在!")
    if not os.path.exists(dst_dir_path):
        print("目的文件夹不存在!\n正在创建文件夹...")
        os.mkdir(dst_dir_path)

    for root, dirs, files in os.walk(src_dir_path, True):
        for eachfile in files:
            shutil.copy(os.path.join(root, eachfile), dst_dir_path)


def create_dir_for_match_files_main(file_dir, ext_list):
    """
    整合型函数
    在file_dir目录下(不遍历下一级目录)，如果有同一场比赛的上、下半场的两个视频视频
    (文件的后缀名在ext_list中)，没有放入同一目录。
    则为这场比赛新建一个目录，然后将这两个视频文件移动到该目录下

    如果该文件没有找到和它类似名称的其他文件，
    说明这个场比赛视频就是完整的一场比赛，没有分上下场
    为其创建一个同名目录，并将这个视频文件移动到目录下

    只在file_dir目录的第一层查找视频文件，子目录中的不处理
    :param file_dir:
    :return:
    """
    for root, dirs, files in os.walk(file_dir):
        # 当遍历file_dir目录时才查看，是否有同一场比赛的上下半场的视频，没有放入同一目录
        if root == file_dir:

            for file in files:
                file_path, file_name_without_ext, extension = \
                    get_filePath_fileName_fileExt(file)
                # 如果文件的后缀名不在指定的后缀名list中，则跳过该文件
                if extension not in ext_list:
                    continue
                #深复制files变量，这样删除里面的元素不会影响files变量(否则会影响for循环)
                compare_files=files[:]
                compare_files.remove(file)
                #参考　https://stackoverflow.com/a/47820184/1314124
                similar_file_list = get_close_matches(file, compare_files, cutoff=0.9)
                if similar_file_list:
                    similar_file_list.append(file)
                    dir_path = create_dir_for_files(file_dir, similar_file_list)
                    move_files_to_dir(root, dir_path, similar_file_list)
                else:
                    # 如果该文件没有找到和它类似名称的其他文件，
                    # 说明这个场比赛视频就是完整的一场比赛，没有分上下场
                    # 为其创建一个同名目录，并将这个视频文件移动到目录下
                    # todo 只为视频文件建立目录
                    file_list = [file, file]
                    dir_path = create_dir_for_files(file_dir, file_list)
                    file_list = [file]
                    move_files_to_dir(root, dir_path, file_list)


def move_files_to_dir_with_dir_structure(src_dir_path, dest_dir_path,
                                         ext_list):
    """
    将指定目录src下的文件夹和文件，移动到指定的目录下dst_dir_path，
    保持src目录下文件夹和文件的结构

    可以指定ext_list列表，指定移动的文件的后缀

    src_dir_path:原目录
    dest_dir_path:目标目录，如果不存在，则建立
    ext_list：文件的后缀列表，只移动指定后缀的文件，比如 ext_list = ['.mkv', '.mp4', '.ts', ]

    参考 https://blog.csdn.net/soslinken/article/details/54015578
    """
    file_info_dict = {}
    for root, dirs, files in os.walk(src_dir_path):
        for file_name in files:
            file_dir, file_name_without_ext, extension = \
                get_filePath_fileName_fileExt(file_name)
            # 如果遍历的目录下的文件后缀名是指定的后缀名exts
            # 则将该文件名保存到file_info_dict字典中
            if extension in ext_list:
                # 如果保存文件信息的字典file_info_dict里，
                # 没有以此次for遍历的目录root为名称的元素，则新建
                if root not in file_info_dict.keys():
                    file_info_dict[root] = []

                file_info_dict[root].append(file_name)
    # 将src目录下，符合条件的目录下的文件，移动到目标dest
    for root, file_names in file_info_dict.items():
        # 在src_dir_path中去除root目录+斜杠后剩下的路径，也就是相对路径
        relativepath = root[len(src_dir_path) + 1:]
        newpath = os.path.join(dest_dir_path, relativepath)
        for file_name in file_names:
            oldfile = os.path.join(root, file_name)
            print("拷贝文件 [" + oldfile + "] 至 [" + newpath + "]")
            # 如果新的目录下，同名的文件newpath不存在，则新建该文件的上一级目录newpath
            # 然后再移动文件到该目录下(注意：文件的目录还在)
            if not os.path.exists(newpath):
                print("新建目录 [" + newpath + "]")
                os.makedirs(newpath)
            # 移动文件到新位置，原来的文件就不存在了
            shutil.move(oldfile, newpath)
        # 移动完文件之后，将src目录下的这些文件所在的目录删除
        print("删除目录 [" + root + "]")
        shutil.rmtree(root)
