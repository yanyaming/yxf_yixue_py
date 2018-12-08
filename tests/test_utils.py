#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from yxf_yixue import Excel2Db, Db, Db2Cdata

if __name__ == '__main__':
    # c = Db2Cdata()
    # print(c.get_wuxing_shengke('木','金'))
    # print(c.get_wuxing_shishen('乙'))
    # d = Db()
    # print(d.get_tabledict_dict('[基础表-六十甲子]'))
    e = Excel2Db()
    e.transform2db()
    pass
