import os

def traversal_files(path, processor):
    """
    遍历处理目录下的所有文件
    :param path: str 目录路径
    :param processor: func 对每个文件的处理函数
    """
    for dir_path in os.listdir(path):
        dir_path = os.path.join(path, dir_path)
        print(dir_path)
        # 判断当前目录为文件夹递归遍历目录
        if os.path.isdir(dir_path):
            traversal_files(dir_path, processor)
        else:
            processor()
