# # -*- coding: utf-8 -*-
# import os
# import re
# import openpyxl
# import openpyxl.utils
#
#
# class Datax:
#     def __init__(self):
#         self.year = 1900
#         self.month = 1
#         self.arr = []
#         for i in range(0, 25):
#             self.arr.append(0)
#
#     def execute_xlsx1(self, typ, path1, path2):
#         realpath1 = os.path.join(os.getcwd(), path1)
#         realpath2 = os.path.join(os.getcwd(), path2)
#         # 读取原始表格
#         wb_origin = openpyxl.load_workbook(realpath1)
#         ws_origin = wb_origin.active
#         # 初始化目标表
#         wb_work, ws_work = eval("self." + self.check(typ) + "_1(realpath2)")  # 根据输入参数动态选取对应函数
#         # 每次循环对应原始表格和目标表格的一行
#         for i, row in enumerate(ws_origin):
#             rows = ws_origin.max_row
#             # 第一行为标题，需跳过
#             if i == 0:
#                 continue
#             # for循环计数从0开始，但表格行列数从1开始，要注意差别
#             # 数据列处理
#             arr = eval("self." + self.check(typ) + "_2(ws_origin, i)")  # 根据输入参数动态选取对应函数
#             # 输出到目标表
#             print(i)
#             ws_work.append(arr)
#         # 保存文件
#         wb_work.save(realpath2)
#
#     def execute_xlsx2(self, typ, path1, path2):
#         realpath1 = os.path.join(os.getcwd(), path1)
#         realpath2 = os.path.join(os.getcwd(), path2)
#         # 读取原始表格
#         wb_origin = openpyxl.load_workbook(realpath1)
#         ws_origin = wb_origin.active
#         # 初始化目标表
#         wb_work, ws_work = eval("self." + self.check(typ) + "_3(ws_origin, realpath2)")
#         # 每次循环对应原始表格和目标表格的一行
#         for i, row in enumerate(ws_origin):
#             rows = ws_origin.max_row
#             # 第一行为标题，需跳过
#             if i == 0:
#                 continue
#             # for循环计数从0开始，但表格行列数从1开始，要注意差别
#             # 数据列处理
#             arr = eval("self." + self.check(typ) + "_4(ws_origin, i)")
#             # 输出到目标表
#             if arr is not None:
#                 print(i)
#                 ws_work.append(arr)
#         # 保存文件
#         wb_work.save(realpath2)
#
#     @staticmethod
#     def check(typ):
#         if typ == "节气":
#             return "jieqi"
#         else:
#             raise ImportError("输入参数错误：typ=" + typ)
#
#     def jieqi_1(self, realpath2):
#         # 若已存在目标表，删除
#         if os.path.exists(realpath2):
#             os.remove(realpath2)
#         # 重新建立目标表格
#         wb_work = openpyxl.Workbook()
#         ws_work = wb_work.active
#         # 输出标题行
#         ws_work.append(
#             ['阳历年',
#              '阳历月',
#              '日表'
#              ])
#         return wb_work, ws_work
#
#     def jieqi_2(self, ws_origin, i):
#         # 当期数据
#         arr = []
#         SY = int(ws_origin[i+1][0].value.split('年')[0])
#         SM = int(ws_origin[i+1][1].value.split('月')[0])
#         RB = ''
#         # 解析html数据
#         div = re.findall(r'<div class="table">(.*?)</div>', ws_origin[i+1][2].value)[0]
#         tbody = re.findall(r'<tbody>(.*?)</tbody>', div)[0]
#         item = re.findall(r'<td class="" data-id="\d+">(.*?)</td>', tbody)
#         for i in item:
#             span1 = re.findall(r'<span class="s1">(.*?)</span>', i)[0]
#             span2 = re.findall(r'<span class="s2">(.*?)</span>', i)[0]
#             RB = RB + span1 + ' ' + span2 + ';'
#         # 以下语句出现死循环，不知道原因。现在没用了
#         # for i in list1:
#         #     SR = SR + str(i) + ' '
#         # for i in list2:
#         #     LR += LR + str(i) + ' '
#         arr.append(SY)
#         arr.extend([SM, RB])
#         return arr
#
#     def jieqi_3(self, realpath2):
#         # 若已存在目标表，删除
#         if os.path.exists(realpath2):
#             os.remove(realpath2)
#         # 重新建立目标表格
#         wb_work = openpyxl.Workbook()
#         ws_work = wb_work.active
#         # 输出标题行
#         ws_work.append(
#             ['阳历年',
#              '小寒',
#              '大寒',
#              '立春',
#              '雨水',
#              '惊蛰',
#              '春分',
#              '清明',
#              '谷雨',
#              '立夏',
#              '小满',
#              '芒种',
#              '夏至',
#              '小暑',
#              '大暑',
#              '立秋',
#              '处暑',
#              '白露',
#              '秋分',
#              '寒露',
#              '霜降',
#              '立冬',
#              '小雪',
#              '大雪',
#              '冬至'
#              ])
#         return wb_work, ws_work
#
#     def jieqi_4(self, ws_origin, i):
#         self.arr[0] = int(ws_origin[i+1][0].value)
#         month = ws_origin[i+1][1].value
#         string = ws_origin[i+1][2].value.rstrip(';')
#         for j in string.split(';'):
#             k = j.split(' ')
#             if k[1] in ['小寒','立春', '惊蛰', '清明','立夏','芒种','小暑', '立秋','白露','寒露','立冬','大雪']:  # 节，上半月，1、3、5
#                 self.arr[month*2-1] = int(j.split(' ')[0])
#             if k[1] in [ '大寒', '雨水','春分','谷雨','小满','夏至','大暑','处暑','秋分', '霜降','小雪','冬至']:  # 气，下半月，2、4、6
#                 self.arr[month*2] = int(j.split(' ')[0])
#         if ws_origin[i+1][1].value == 12:
#             arr = self.arr.copy()
#             for j in range(0, 25):
#                 self.arr[j] = 0
#             return arr
#         else:
#             return None
