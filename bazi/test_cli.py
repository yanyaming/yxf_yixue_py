#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from paipan import Paipan
from bazi.fenxi import Fenxi
from bazi import bazi_api
from wannianli import wannianli_api


if __name__ == '__main__':
    a = bazi_api.Api()
    jingdu = 120
    string = '1996/02/29 23:16'
    obj = datetime.datetime(1996, 7, 12, 12, 40)
    print(a.paipan(obj, xingbie='男'))
    a.print_pan()
    # a.get_lianghuafenxi()
    pass
