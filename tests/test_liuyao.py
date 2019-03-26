#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from yxf_yixue.liuyao import LiuyaoApi


if __name__ == '__main__':
    string = '1996/02/29 23:16'
    obj = datetime.datetime(2018, 6, 24, 21, 40)
    a = LiuyaoApi()
    res1 = a.paipan(obj, qiguafangfa='两数字起卦', qiguashuru=[5, 9], naganzhifangfa='传统京氏')
    print(a.print_pan())
    # res = a.get_danqishikongfa(obj, qiguashuru=[1])
    # print(res)
    pass
