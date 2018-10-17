# -*- coding: utf-8 -*-
import settings
import os
import sys
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
