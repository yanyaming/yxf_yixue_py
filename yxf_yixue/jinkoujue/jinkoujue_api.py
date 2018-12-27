#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..wannianli import WannianliApi
from ._paipan import Paipan
from ._fenxi import Chuantongfenxi, Lianghuafenxi


class JinkoujueApi:
    def __init__(self):
        self.p = None
        self.zhanshi = None
        self.pan = None
        self.ke = None
        self.chuantongfenxi = None
        self.lianghuafenxi = None

    def paipan(self, datetime_obj, difen='子', yuejiang=None, zhanshi=None):
        a = WannianliApi()
        self.p = Paipan()
        calendar = a.get_Calendar(datetime_obj)
        self.pan = self.p.paipan(calendar[3], difen=difen, yuejiang=yuejiang, zhanshi=zhanshi)
        return self.pan

    def print_pan(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        else:
            if self.pan.get('标签', None):
                if self.pan['标签'] == '传统分析':
                    output = self.p.output()
                    output += self.chuantongfenxi.output_addition()
                    return output
                elif self.pan['标签'] == '量化分析':
                    output = self.p.output()
                    output += self.lianghuafenxi.output_addition()
                    return output
            else:
                return self.p.output()

    def get_chuantongfenxi(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.chuantongfenxi = Chuantongfenxi()
        self.zhanshi, self.pan, self.ke = self.chuantongfenxi.fenxi(self.zhanshi, self.pan, self.ke)
        return [self.zhanshi, self.pan, self.ke]

    def get_lianghuafenxi(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.lianghuafenxi = Lianghuafenxi()
        self.zhanshi, self.pan, self.ke = self.lianghuafenxi.fenxi(self.zhanshi, self.pan, self.ke)
        return [self.zhanshi, self.pan, self.ke]
