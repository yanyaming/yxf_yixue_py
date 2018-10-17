#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
import jinkoujue.paipan as paipan
import jinkoujue.fenxi as fenxi
import jinkoujue.jinkoujue_api as api


if __name__ == '__main__':
    string = '1996/02/29 23:16'
    obj = datetime.datetime(2018, 6, 26, 20, 40)
    a = api.Api()
    res1 = a.paipan(obj, difen='酉')
    print(res1)
    a.print_pan()
    pass

