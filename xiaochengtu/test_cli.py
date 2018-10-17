#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
import xiaochengtu.paipan as paipan
import xiaochengtu.fenxi as fenxi
import xiaochengtu.xiaochengtu_api as api


if __name__ == '__main__':
    string = '1996/02/29 23:16'
    obj = datetime.datetime(2012, 3, 7, 17, 40)
    a = api.Api()
    res1 = a.paipan(obj)
    print(res1)
    a.print_pan()
    res2 = a.get_chuantongfenxi()
    print(res2)
