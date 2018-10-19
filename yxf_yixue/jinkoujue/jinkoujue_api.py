#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..wannianli import WannianliApi
from ._paipan import Paipan
from ._fenxi import Fenxi


class JinkoujueApi:
    def __init__(self):
        self.p = None

    def paipan(self, datetime_obj, difen, yuejiang=None, zhanshi=None):
        a = WannianliApi()
        self.p = Paipan()
        return_list = a.get_Calendar(datetime_obj)
        res = self.p.paipan(return_list[3], difen=difen, yuejiang=yuejiang, zhanshi=zhanshi)
        return res

    def print_pan(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.p.output()
