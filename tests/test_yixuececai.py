#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os  # 系统命令
import sys  # python设置
import shutil  # 高级文件操作
import timeit  # 计时相关
import datetime
import time  # 时间相关
import random
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
from yxf_yixue.app_yixuececai.jichufenxi import Pr,P,Cr,C
from yxf_yixue.app_yixuececai.datax import *
from yxf_yixue.app_yixuececai.yuce import *


def work1():
    pass


def work2():
    pass


def work3():
    # 测试八字喜用五行的命中率
    yuce = Yuce()
    yuce.test_bazi()


def work4():
    # 投注分析
    print('理论出组六概率：')
    print(P(10,3)/Pr(10,3))
    print('组六包7理论中奖概率：')
    print(C(4,3)*P(3,3)/Pr(10,3))
    # print(Pr(10, 3, True))
    pass


if __name__ == '__main__':
    print("基础路径：", BASE_DIR)
    # gen_db()  # 生成数据库，只需要在最初执行一次
    work3()