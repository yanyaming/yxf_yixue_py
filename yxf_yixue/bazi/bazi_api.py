#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..wannianli import wannianli_api
from ._paipan import Paipan
from ._fenxi import Chuantongfenxi, Lianghuafenxi


class BaziApi:
    def __init__(self):
        self.P = None
        self.pan = None
        self.chuantongfenxi = None
        self.lianghuafenxi = None

    def paipan(self, datetime_obj, xingbie='男'):
        a = wannianli_api.WannianliApi()
        self.P = Paipan()
        calendar = a.get_Calendar(datetime_obj)
        solarTermJie = a.get_SolarTermJie(datetime_obj)
        self.pan = self.P.paipan(datetime_obj, calendar, solarTermJie, xingbie=xingbie)
        return self.pan

    def print_pan(self):
        if self.paipan is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        else:
            if self.pan.get('标签', None):
                if self.pan['标签'] == '传统分析':
                    output = self.P.output()
                    output += self.chuantongfenxi.output_addition()
                    return output
                elif self.pan['标签'] == '量化分析':
                    output = self.P.output()
                    output += self.lianghuafenxi.output_addition()
                    return output
            else:
                return self.P.output()

    def get_chuantongfenxi(self):
        if self.P is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.chuantongfenxi = Chuantongfenxi()
        self.pan = self.chuantongfenxi.fenxi(self.pan)
        return self.pan

    def get_lianghuafenxi(self):
        if self.P is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.lianghuafenxi = Lianghuafenxi()
        self.pan = self.lianghuafenxi.fenxi(self.pan)
        return self.pan
