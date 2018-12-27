#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from yxf_yixue.bazi import BaziApi
from yxf_yixue.wannianli import WannianliApi


if __name__ == '__main__':
    a = BaziApi()
    string = '1996/02/29 23:16'
    obj = datetime.datetime(1996, 7, 12, 12, 40)
    print(a.paipan(obj, xingbie='男'))
    print(a.print_pan())
    # a.get_lianghuafenxi()
    pass
