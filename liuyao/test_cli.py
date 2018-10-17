#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
import liuyao.paipan as paipan
import liuyao.fenxi as fenxi
import liuyao.liuyao_api as api


if __name__ == '__main__':
    string = '1996/02/29 23:16'
    obj = datetime.datetime(2018, 6, 24, 21, 40)
    a = api.Api()
    res1 = a.paipan(obj, qiguafangfa='爻位起卦', qiguashuru=[5, 1, 8, 5, 4, 8, [4]], naganzhifangfa='传统京氏')
    print(res1)
    a.print_pan()
    # res = a.get_danqishikongfa(obj, qiguashuru=[1])
    # print(res)
    pass