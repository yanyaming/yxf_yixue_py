#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 基地址是本项目根目录
sys.path.append(BASE_DIR)
import datetime
from yxf_yixue.wannianli import WannianliApi
from yxf_yixue.wannianli._realsolar import RealSolar
from yxf_yixue.wannianli._calendar import Calendar


if __name__ == '__main__':
    # 测试通过
    jingdu = 150
    datetime_str = '1996/02/29 23:16'
    datetime_obj = datetime.datetime(2018,12,27,0,20)

    t = WannianliApi()
    # print(t.get_BeijingshijianNow(zhidinggeshi='%Y-%m-%d %H:%M:%S'))
    # print(t.get_Heluoshijian(zhidingshijian=datetime_obj))
    # print(t.get_Realsolar(zhidingshijian=datetime_str,jingdu=jingdu))
    print(t.get_SolarTermJie(datetime_obj))
    print(t.get_SolarTermDays(datetime_obj))
    print(t.get_Calendar(datetime_obj,return_fengshui=False,return_zhongyi=False,return_huangji=False))
    # print(t.get_GanzhiYears())
    # print(t.get_GanzhiOneYear())
    # print(t.get_GanzhiOneMonth(2018,12))
    # print(t.get_GanzhiOneDay(datetime_obj))
