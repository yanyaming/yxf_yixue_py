#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os  # 系统命令
import sys  # python设置
import shutil  # 高级文件操作
import timeit  # 计时相关
from datetime import datetime  # 日期时间
import time  # 时间相关
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
from app_yixuecegu.datax import *


class Test:
    def __init__(self):
        pass

    def work1(self):
        pass

    def work2(self):
        pass

    def work3(self):
        pass

    def work4(self):
        pass


if __name__ == '__main__':
    print("基础路径：", BASE_DIR)
    t = Test()
    # gen_db()  # 生成数据库，只需要在最初执行一次
    t.work3()