#!/usr/bin/python3
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals  # Unicode字符集支持。不需要再像py2中那样声明u'str'或b'str'
# from __future__ import print_function  # 新的print()函数
# from __future__ import absolute_import  # 绝对路径导入
# from __future__ import division  # 新的除法。旧的py2:3/2 == 1, 3//2 == 1; 新的py3:3/2 == 1.5, 3//2 == 1
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)

from utils import *
import wannianli.wannianli_api
import bazi.bazi_api
import jinkoujue.jinkoujue_api
import liuyao.liuyao_api
import xiaochengtu.xiaochengtu_api