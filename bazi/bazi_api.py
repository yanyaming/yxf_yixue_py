#!/usr/bin/python3
# -*- coding: utf-8 -*-
import wannianli.wannianli_api
from bazi.paipan import Paipan


class Api:
    def __init__(self):
        self.p = None

    def paipan(self, datetime_obj, xingbie='男'):
        a = wannianli.wannianli_api.Api()
        self.p = Paipan()
        calendar = a.get_Calendar(datetime_obj)
        solarTermJie = a.get_SolarTermJie(datetime_obj)
        Info = self.p.paipan(datetime_obj, calendar, solarTermJie, xingbie=xingbie)
        return Info

    def print_pan(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.p.output()

    def get_lianghuafenxi(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        s = None
        return s
