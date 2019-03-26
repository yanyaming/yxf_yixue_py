#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import web
import sys
import json
import os
import re
import datetime
import logging
WEB_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(WEB_ROOT)
from yxf_yixue import WannianliApi,BaziApi,JinkoujueApi,XiaochengtuApi,LiuyaoApi,QimenApi


# 网址路由
urls = (
    '/wannianli', 'wannianli',
    '/bazi', 'bazi',
    '/jinkoujue', 'jinkoujue',
    '/liuyao', 'liuyao',
    '/xiaochengtu', 'xiaochengtu',
    '/qimen', 'qimen',
)


# 中间件：接收到请求后最先执行，返回日期时间对象，若出错则直接响应错误代码
def middleware_check_datetime(date,time):
    if date and time:
        dt_str = date + ' ' + time
        try:
            if re.findall(r'-', date):
                dt_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
                return dt_obj
            elif re.findall(r'/', date):
                dt_obj = datetime.datetime.strptime(dt_str, '%Y/%m/%d %H:%M')
                return dt_obj
            else:
                return middleware_before_return(res=None,message='日期时间格式错误')  # 没有匹配到-和/
        except Exception as e:
            return middleware_before_return(res=None,message='日期时间转换出错')  # 转换出错
    else:
        return middleware_before_return(res=None,message='没有输入日期时间参数')  # 没有此参数


# 中间件：判断应该如何返回给客户端，完成响应
def middleware_before_return(res=None,op='json',message='错误的请求'):
    err_output = {'status': 400, 'message': message}
    if res:
        if op == 'json':
            json_result = json.dumps(res, ensure_ascii=False)
        else:
            json_result = res
    else:
        json_result = err_output
    web.header("Access-Control-Allow-Origin", "*")
    return json_result


# 视图：万年历
class wannianli(object):
    def GET(self):
        inputs = web.input()
        print(str(datetime.datetime.now()) + str(inputs))
        # 必要参数
        op = inputs.get('op', None)  # 返回何种格式。固定选项：json/str
        date = inputs.get('date', None)  # 提交的查询日期。固定格式：YYYY-mm-dd（若格式不严谨可二次处理，例如YYYY-M-D,YYYY/mm/dd）
        time = inputs.get('time', None)  # 提交的查询时间。固定格式：HH:MM
        dt_obj = middleware_check_datetime(date,time)
        if not isinstance(dt_obj,datetime.datetime):
            return dt_obj
        # 可选参数
        subop = inputs.get('subop', None)  # 子操作。所有类别都需要，不写返回默认值
        jingdu = inputs.get('jingdu', None)  # 万年历需要。数字：仅限东经0-180
        return_fengshui = inputs.get('return_fengshui', False)  # 万年历需要。逻辑：True/False
        return_zhongyi = inputs.get('return_zhongyi', False)  # 万年历需要。逻辑：True/False
        return_huangji = inputs.get('return_huangji', False)  # 万年历需要。逻辑：True/False
        if return_fengshui=='True':
            return_fengshui=True
        elif return_fengshui=='False':
            return_fengshui=False
        if return_zhongyi=='True':
            return_zhongyi=True
        elif return_zhongyi=='False':
            return_zhongyi=False
        if return_huangji=='True':
            return_huangji=True
        elif return_huangji=='False':
            return_huangji=False
        start_year = inputs.get('start_year', False)  # 万年历需要。数字大于等于1900
        end_year = inputs.get('end_year', False)  # 万年历需要。数字小于等于2100
        year = inputs.get('year',None)  # 万年历需要。数字1900-2100
        month = inputs.get('month',None)  # 万年历需要。数字1-12
        # 执行数术程序
        c = WannianliApi()
        dt_obj_c = dt_obj
        res = None
        try:
            if jingdu:
                dt_obj_c = c.get_Realsolar(zhidingshijian=dt_obj,jingdu=int(jingdu))['时间']
            if subop is None or subop == 'get_Calendar':
                if op == 'str':
                    res = c.get_Calendar(dt_obj_c, return_fengshui=return_fengshui, return_zhongyi=return_zhongyi,return_huangji=return_huangji,return_type='str')
                elif op == 'json':
                    res = c.get_Calendar(dt_obj_c,return_fengshui=return_fengshui,return_zhongyi=return_zhongyi,return_huangji=return_huangji,return_type='json')
                else:
                    res = c.get_Calendar(dt_obj_c, return_fengshui=return_fengshui, return_zhongyi=return_zhongyi,return_huangji=return_huangji, return_type='origin')
            elif subop == 'get_GanzhiYears':
                res = c.get_GanzhiYears(start_year=int(start_year),end_year=int(end_year))
            elif subop == 'get_GanzhiOneYear':
                res = c.get_GanzhiOneYear(year=int(year))
            elif subop == 'get_GanzhiOneMonth':
                res = c.get_GanzhiOneMonth(year=int(year),month=int(month))
            elif subop == 'get_GanzhiOneDay':
                res = c.get_GanzhiOneDay(dt_obj_c)
        except Exception as e:
            print(e)
        return middleware_before_return(res,op)


# 视图：八字
class bazi(object):
    def GET(self):
        inputs = web.input()
        print(str(datetime.datetime.now()) + str(inputs))
        # 必要参数
        op = inputs.get('op', None)  # 返回何种格式。固定选项：json/str
        date = inputs.get('date', None)  # 提交的查询日期。固定格式：YYYY-mm-dd（若格式不严谨可二次处理，例如YYYY-M-D,YYYY/mm/dd）
        time = inputs.get('time', None)  # 提交的查询时间。固定格式：HH:MM
        dt_obj = middleware_check_datetime(date, time)
        if not isinstance(dt_obj,datetime.datetime):
            return dt_obj
        # 可选参数
        subop = inputs.get('subop', None)  # 子操作。所有类别都需要，不写返回默认值
        xingbie = inputs.get('xingbie', '男')  # 八字需要。汉字：男/女
        # 执行数术程序
        c = BaziApi()
        res = None
        try:
            if subop is None or subop == '排盘':
                res = c.paipan(dt_obj, xingbie=xingbie)
                if op == 'str':
                    res = c.print_pan()
            elif subop == '传统分析':
                c.paipan(dt_obj, xingbie=xingbie)
                res = c.get_chuantongfenxi()
                if op == 'str':
                    res = c.print_pan()
            elif subop == '量化分析':
                c.paipan(dt_obj, xingbie=xingbie)
                res = c.get_lianghuafenxi()
                if op == 'str':
                    res = c.print_pan()
        except Exception as e:
            print(e)
        return middleware_before_return(res, op)


# 视图：金口诀
class jinkoujue(object):
    def GET(self):
        inputs = web.input()
        print(str(datetime.datetime.now()) + str(inputs))
        # 必要参数
        op = inputs.get('op', None)  # 返回何种格式。固定选项：json/str
        date = inputs.get('date', None)  # 提交的查询日期。固定格式：YYYY-mm-dd（若格式不严谨可二次处理，例如YYYY-M-D,YYYY/mm/dd）
        time = inputs.get('time', None)  # 提交的查询时间。固定格式：HH:MM
        dt_obj = middleware_check_datetime(date, time)
        if not isinstance(dt_obj,datetime.datetime):
            return dt_obj
        # 可选参数
        subop = inputs.get('subop', None)  # 子操作。所有类别都需要，不写返回默认值
        difen = inputs.get('difen', '子')  # 金口诀需要。汉字：十二地支之一
        yuejiang = inputs.get('yuejiang', None)  # 金口诀需要。汉字：十二地支之一
        zhanshi = inputs.get('zhanshi', None)  # 金口诀需要。汉字：十二地支之一
        # 执行数术程序
        c = JinkoujueApi()
        res = None
        try:
            if subop is None or subop == '排盘':
                res = c.paipan(dt_obj,difen=difen,yuejiang=yuejiang,zhanshi=zhanshi)
                if op == 'str':
                    res = c.print_pan()
            elif subop == '传统分析':
                c.paipan(dt_obj,difen=difen,yuejiang=yuejiang,zhanshi=zhanshi)
                res = c.get_chuantongfenxi()
                if op == 'str':
                    res = c.print_pan()
            elif subop == '量化分析':
                c.paipan(dt_obj,difen=difen,yuejiang=yuejiang,zhanshi=zhanshi)
                res = c.get_lianghuafenxi()
                if op == 'str':
                    res = c.print_pan()
        except Exception as e:
            print(e)
        return middleware_before_return(res, op)


# 视图：六爻
class liuyao(object):
    def GET(self):
        inputs = web.input()
        print(str(datetime.datetime.now()) + str(inputs))
        # 必要参数
        op = inputs.get('op', None)  # 返回何种格式。固定选项：json/str
        date = inputs.get('date', None)  # 提交的查询日期。固定格式：YYYY-mm-dd（若格式不严谨可二次处理，例如YYYY-M-D,YYYY/mm/dd）
        time = inputs.get('time', None)  # 提交的查询时间。固定格式：HH:MM
        dt_obj = middleware_check_datetime(date, time)
        if not isinstance(dt_obj,datetime.datetime):
            return dt_obj
        # 可选参数
        subop = inputs.get('subop', None)  # 子操作。所有类别都需要，不写返回默认值
        qiguafangfa = inputs.get('qiguafangfa', '标准时间起卦')  # 六爻需要。汉字：具体看代码
        qiguashuru = inputs.get('qiguashuru', None)  # 六爻需要。逗号隔开的数字字符串：具体看代码
        naganzhifangfa = inputs.get('naganzhifangfa', '传统京氏')  # 六爻需要。汉字：传统京氏/先天甲子易
        # 执行数术程序
        c = LiuyaoApi()
        res = None
        try:
            if subop is None or subop == '排盘':
                res = c.paipan(dt_obj, qiguafangfa=qiguafangfa, qiguashuru=qiguashuru,naganzhifangfa=naganzhifangfa)
                if op == 'str':
                    res = c.print_pan()
        except Exception as e:
            print(e)
        return middleware_before_return(res, op)


# 视图：小成图
class xiaochengtu(object):
    def GET(self):
        inputs = web.input()
        print(str(datetime.datetime.now())+str(inputs))
        # 必要参数
        op = inputs.get('op', None)  # 返回何种格式。固定选项：json/str
        date = inputs.get('date', None)  # 提交的查询日期。固定格式：YYYY-mm-dd（若格式不严谨可二次处理，例如YYYY-M-D,YYYY/mm/dd）
        time = inputs.get('time', None)  # 提交的查询时间。固定格式：HH:MM
        dt_obj = middleware_check_datetime(date, time)
        if not isinstance(dt_obj,datetime.datetime):
            return dt_obj
        # 可选参数
        subop = inputs.get('subop', None)  # 子操作。所有类别都需要，不写返回默认值
        lingdongshu = inputs.get('lingdongshu', None)  # 小成图需要。数字：任意整数
        shuziqigua = inputs.get('shuziqigua', None)  # 小成图需要。逻辑：True/False
        guizangfangfa = inputs.get('guizangfangfa', '四正')  # 小成图需要。汉字：具体看代码
        # 执行数术程序
        c = XiaochengtuApi()
        res = None
        try:
            if subop is None or subop == '排盘':
                res = c.paipan(dt_obj, lingdongshu=lingdongshu, shuziqigua=shuziqigua,guizangfangfa=guizangfangfa)
                if op == 'str':
                    res = c.print_pan()
        except Exception as e:
            print(e)
        return middleware_before_return(res, op)


# 视图：奇门
class qimen(object):
    def GET(self):
        inputs = web.input()
        print(str(datetime.datetime.now()) + str(inputs))
        # 必要参数
        op = inputs.get('op', None)  # 返回何种格式。固定选项：json/str
        date = inputs.get('date', None)  # 提交的查询日期。固定格式：YYYY-mm-dd（若格式不严谨可二次处理，例如YYYY-M-D,YYYY/mm/dd）
        time = inputs.get('time', None)  # 提交的查询时间。固定格式：HH:MM
        dt_obj = middleware_check_datetime(date, time)
        if not isinstance(dt_obj, datetime.datetime):
            return dt_obj
        # 可选参数
        subop = inputs.get('subop', None)  # 子操作。所有类别都需要，不写返回默认值
        bujufangfa = inputs.get('bujufangfa','飞盘')  # 奇门需要。汉字：转盘/飞盘
        # 执行数术程序
        c = QimenApi()
        res = None
        try:
            if subop is None or subop == '排盘':
                res = c.paipan(dt_obj, bujufangfa=bujufangfa)
                if op == 'str':
                    res = c.print_pan()
            elif subop == '传统分析':
                c.paipan(dt_obj, bujufangfa=bujufangfa)
                res = c.get_chuantongfenxi()
                if op == 'str':
                    res = c.print_pan()
        except Exception as e:
            print(e)
        return middleware_before_return(res, op)


# 运行服务
if __name__ == '__main__':
    sys.argv.append('0.0.0.0:8002')
    app = web.application(urls, globals())
    app.run()
