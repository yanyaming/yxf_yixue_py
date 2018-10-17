# -*- coding: utf-8 -*-
import settings
import os
import sys
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

