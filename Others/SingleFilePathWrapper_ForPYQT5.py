# coding = utf8

import os
import sys

os.path.abspath(".")


def resource_path(absolute_path):
    """
        如果PyQt5 打包的是单文件，因为单文件的导入形式是以压缩/解压的形式存储的Temporary，
        每一次的路径都是不同的，需要使用该包装器将路径传入，再获得临时路径再传回
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, absolute_path)


if __name__ == "__main__":
    path = r"D:\PycharmProjects\pythonProject_seevision\dolphingscript\串口驱动_串口控制相机麦克风等的log_androidlog独立开"
    print(resource_path(path))
