# -*- coding:utf-8 -*-
import os
import re

test_str = "11 # asdfafdasdf"  # 12111


class FileProcessor:

    @classmethod
    def remove_pound_sign(cls, file_data, path):
        """
        # '#' 开头的注释
        排除 # -*- coding:utf-8 -*-
        :param file_data:
        :param path:
        :return: f
        """
        re_start = r"^\s*#"
        data = []  # data
        for line in file_data:
            if not re.search(re_start, line) and not re.match(r'# -\*- coding:utf-8 -\*-', line):
                data.append(line)
        return '\n'.join(data)

    @classmethod
    def remove_quotes(cls, file_data, path):
        """
        # ''' 或 \""" 开头的注释
        :param file_data:
        :param path:
        :return: f
        """
        single_quotes_start = r"^\s*'''"
        single_quotes_end = r"'''\s*\n$"
        double_quotes_start = r'^\s*"""'
        double_quotes_end = r'"""\s*\n$'

        # 检测开始与结束
        single_quotes_mark = False
        double_quotes_mark = False

        data = []
        for line in file_data:
            if re.search(single_quotes_start, line) and not single_quotes_mark:
                # ''' 开始
                # print 1, line
                single_quotes_mark = True
            elif re.search(double_quotes_start, line) and not double_quotes_mark:
                # """ 开始
                # print 2, line
                double_quotes_mark = True

            if (not single_quotes_mark) and (not double_quotes_mark):
                # 添加非注释内的的行
                data.append(line)

            if re.search(single_quotes_end, line) and single_quotes_start:
                # ''' 结束
                # print 3, line
                single_quotes_mark = False
            elif re.search(double_quotes_end, line) and double_quotes_start:
                # """ 结束
                # print 4, line
                double_quotes_mark = False

        if single_quotes_mark or double_quotes_mark:
            print single_quotes_mark, double_quotes_mark
            print '{}有问题'.format(path)
        return '\n'.join(data)

    @classmethod
    def remove_blank_line(cls, file_data, path):
        """
        # 删除空行 删除只有空格的行
        :param file_data:
        :param path:
        :return: f
        """
        re_p = r'^\s*\n$'
        data = []
        for line in file_data:
            if not re.search(re_p, line):
                data.append(line)
        return '\n'.join(data)

    @classmethod
    def main(cls, file_data, path):
        """
        主程序
        """
        f = cls.remove_quotes(file_data, path)
        f = cls.remove_pound_sign(f, path)
        f = cls.remove_blank_line(f, path)
        return f


def traversal_files(path):
    for dir_path in os.listdir(path):
        dir_path = os.path.join(path, dir_path)
        print(dir_path)
        # 判断当前目录为文件夹递归遍历目录
        if os.path.isdir(dir_path):
            traversal_files(dir_path)
        elif re.search(r".p1y$", dir_path):
            # 处理.py文件
            with open(dir_path, 'r') as f:
                new_f = FileProcessor.remove_quotes(f, dir_path)
                print new_f
            with open(dir_path, 'w') as f:
                f.write(new_f)


