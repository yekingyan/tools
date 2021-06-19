import os


def traversal_files(processor, path=".", is_include_dir=False):
    """
    遍历处理目录下的所有文件（可选是否处理文件夹）
    :param path: str 目录路径
    :param processor: func 对每个文件的处理函数
    :param is_include_dir: 是否处理文件夹
    """
    if not os.path.exists(path):
        print("不存在路径", os.path.abspath(path))
        return
    for dir_path in os.listdir(path):
        dir_path = os.path.join(path, dir_path)
        # 判断当前目录为文件夹递归遍历目录
        if os.path.isdir(dir_path):
            if is_include_dir:
                processor(dir_path)
            traversal_files(processor, dir_path)
        else:
            file_name = dir_path
            processor(file_name)


def replace_filename(src_name, dst_name, path=".", is_include_dir=False):
    """
    批量更替文件名
    :param path: str 父目录
    :param src_name: str 需要更替的字符串
    :param dst_name: str 更替成的字符串
    :param is_include_dir: 是否处理文件夹名称

    >>> open(".", "ab_ccc_d.txt").close()
    >>> replace_filename("ccc", "ddd")
    >>> assert os.path.exists("ab_ddd_d.txt")
    """

    def _replace_filename(_src_name, _dst_name):
        def wrap(filename):
            origin_name = os.path.join(path, filename)
            new_name = os.path.join(path, filename.replace(_src_name, _dst_name))
            os.rename(origin_name, new_name)

        return wrap

    traversal_files(_replace_filename(src_name, dst_name), path, is_include_dir)

