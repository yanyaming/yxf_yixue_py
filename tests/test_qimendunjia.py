#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from yxf_yixue.qimen import QimenApi


if __name__ == '__main__':
    a = QimenApi()
    obj = datetime.datetime(2011, 12, 22, 20, 40)
    a.paipan(obj)
    res = a.get_cecaifenxi(shangqijianghao=[7,7,2])
    print(a.print_pan())
    print(res['测彩分析']['建议投注'])
    pass
