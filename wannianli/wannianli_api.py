#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import datetime
from wannianli.realsolar import RealSolar
from wannianli.calendar import Calendar

"""
1.时间换算类
2.历法类（公历、农历、数术流运、四柱）
3.对外接口、可变输出API类
"""


class Api:
    def __init__(self):
        pass

    def get_GanzhiYears(self, start_year=1900, end_year=2100):
        # 输入：起止年份
        # 输出：对应年份和年干支
        res = []
        ganzhi = Calendar.Ganzhilifa()
        solarterm = Calendar.SolarTerm()
        for y in range(start_year, end_year + 1):
            dt = datetime.datetime(y,5,1)
            solarterm_str = solarterm.solarTerm(dt)
            ganzhi_year = ganzhi.ganzhi(dt,solarterm_str).split('：')[1][0:2]
            res.append([y,ganzhi_year])
        return res

    def get_GanzhiOneYear(self, year):
        res = []
        ganzhi = Calendar.Ganzhilifa()
        solarterm = Calendar.SolarTerm()
        solartermdays = solarterm.solarTermDays(datetime.datetime(year,5,1))
        for m in range(1, 13):
            dt = datetime.datetime(year, m, int(solartermdays[m-1]))
            solarterm_str = solarterm.solarTerm(dt)
            ganzhi_str = ganzhi.ganzhi(dt, solarterm_str).split('：')[1][2:5]
            res.append([m, ganzhi_str])
        return res

    def get_GanzhiOneMonth(self, year, month):
        pass

    def get_GanzhiOneDay(self, dt):
        pass

    def get_OneDay_lunar2Solar(self, lunar):
        pass

    def get_Realsolar(self, zhidingshijian=None, jingdu=120, zhidinggeshi=None):
        r = RealSolar()
        dt_rs, jingdu_str = r.zhentaiyangshi(zhidingshijian=zhidingshijian, jingdu=jingdu, zhidinggeshi=zhidinggeshi)
        return dt_rs, jingdu_str

    # 阳历、阴历、节气、干支必选，其余可选
    def get_Calendar(self, datetime_obj, return_fengshui=False, return_zhongyi=False, return_huangji=False):
        w = Calendar()
        solar = w.Solar().solar(datetime_obj)
        lunar = w.Lunar().lunar(datetime_obj)
        solarTerm = w.SolarTerm().solarTerm(datetime_obj)
        ganzhi = w.Ganzhilifa().ganzhi(datetime_obj, solarTerm)
        fengshui = None
        if return_fengshui is True:
            fengshui = w.Fengshuilifa().fengshui(datetime_obj,solarTerm,ganzhi)
        zhongyi = None
        if return_zhongyi is True:
            zhongyi = w.Zhongyilifa().zhongyi(solarTerm,ganzhi)
        huangji = None
        if return_huangji is True:
            huangji = w.Huangjilifa().huangjijingshi(datetime_obj,solarTerm)
        return solar,lunar,solarTerm,ganzhi,fengshui,zhongyi,huangji

    def get_SolarTermJie(self, datetime_obj):
        w = Calendar()
        res = w.SolarTerm().solarTermJie(datetime_obj)
        return res

    def get_Today(self, jingdu=120):
        pass

    def get_Now(self, jingdu=120):
        w = self.get_Calendar(datetime.datetime.today(),True,True,True)
        return w
