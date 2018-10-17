#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from wannianli.wannianli_api import Api
from wannianli.calendar import Calendar
from wannianli.realsolar import RealSolar


class Test:
    def __init__(self):
        pass

    def work1(self):
        w = Calendar()
        string = '1996/02/29 23:16'
        obj = datetime.datetime(2018, 10, 17, 2, 40)
        solar = w.Solar().solar(obj)
        print(solar)
        lunar = w.Lunar().lunar(obj)
        print(lunar)
        solarterm = w.SolarTerm().solarTerm(obj)
        print(solarterm)
        solartermjie = w.SolarTerm().solarTermJie(obj)
        print(solartermjie)
        solartermd = w.SolarTerm().solarTermDays(obj)
        print(solartermd)
        ganzhi = w.Ganzhilifa().ganzhi(obj,solarterm)
        print(ganzhi)
        fengshui = w.Fengshuilifa().fengshui(obj,solarterm,ganzhi)
        print(fengshui)
        zhongyi = w.Zhongyilifa().zhongyi(solarterm,ganzhi)
        print(zhongyi)
        huangji = w.Huangjilifa().huangjijingshi(obj,solarterm)
        print(huangji)

    def work2(self):
        api = Api()
        string = '1996/02/29 23:16'
        obj = datetime.datetime(2014, 10, 18, 13, 40)
        dt, jingdu_str = api.get_Realsolar(obj)
        result = api.get_Calendar(dt, return_fengshui=True,return_zhongyi=True, return_huangji=True)
        print(result)
        y = api.get_GanzhiYears()
        print(y)
        m = api.get_GanzhiOneYear(2018)
        print(m)
        r = api.get_Now()
        print(r)

    def work3(self):
        r = RealSolar()
        jingdu = 150
        string = '1996/02/29 23:16'
        obj = datetime.datetime.today()
        print('当前北京时间：' + str(r.beijingshijian_now(zhidinggeshi='%Y/%m/%d %H:%M')))
        print('当前河洛时间：' + str(r.heluoshijian(zhidinggeshi='%Y/%m/%d %H:%M')))
        print('输入时间的河洛时间：' + str(r.heluoshijian(string, zhidinggeshi='%Y/%m/%d %H:%M')))
        print('经度' + str(jingdu) + '的真太阳时：' + str(r.zhentaiyangshi(string, jingdu, zhidinggeshi='%Y/%m/%d %H:%M')))


if __name__ == '__main__':
    t = Test()
    t.work1()
    t.work2()
    t.work3()
