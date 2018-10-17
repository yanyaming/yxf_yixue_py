# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Unicode字符集支持。不需要再像py2中那样声明u'str'或b'str'
from __future__ import print_function  # 新的print()函数
from __future__ import absolute_import  # 绝对路径导入
from __future__ import division  # 新的除法。旧的py2:3/2 == 1, 3//2 == 1; 新的py3:3/2 == 1.5, 3//2 == 1
import os
import platform

BASE_DIR = os.path.dirname(__file__)  # 基地址是本项目根目录
OS = platform.system()  # 返回字符串"Windows" or "Linux"

