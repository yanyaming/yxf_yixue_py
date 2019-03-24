import os
import datetime
from ..utils._db import Db
from ..bazi.bazi_api import BaziApi
from ..qimen.qimen_api import QimenApi
from ..app_yixuececai.jichufenxi import Pr,P,Cr,C


class Yuce:
    def __init__(self):
        self.db = Db('app_yixuececai.db')

    def test_bazi(self):
        fucai3d = self.db.get_tabledict_list("[福彩3D]")
        tongji = {'已执行': 0, '匹配1': 0, '匹配2': 0, '匹配3': 0, '概率1': 0, '概率2': 0, '概率3': 0, '匹配列表': []}

        def get_qushu(table_row0):
            dt_obj = datetime.datetime.strptime(table_row0, '%Y-%m-%d')
            dt_obj += datetime.timedelta(hours=21, minutes=30)
            bazi = BaziApi()
            bazi.paipan(dt_obj, xingbie='男')
            res = bazi.get_lianghuafenxi()
            baziqushu_list = [
                res['量化分析']['建议取数'][0],
                res['量化分析']['建议取数'][1],
                res['量化分析']['建议取数'][2],
                res['量化分析']['建议取数'][3]
            ]
            return baziqushu_list

        # 逐条解析历史数据，每一条都会调用一次预测功能
        for table_row in fucai3d:
            print(table_row)
            baziqushu = get_qushu(table_row['开奖日期'])
            print(baziqushu)
            pipei = []
            # 筛选，为了减少投注数放弃组三，只要是组三号就规定为一个都不匹配
            if table_row['百位'] == table_row['十位'] or table_row['十位'] == table_row['个位'] or table_row['百位'] == table_row['个位']:
                pass
            else:
                for num in table_row['中奖号码'].split(' '):
                    if num in baziqushu:  # 这里的八字取数和中奖号码都是str
                        pipei.append(num)
            print(pipei)
            # 记录数据
            tongji['匹配列表'].append(pipei)
            tongji['已执行'] += 1

        # 全部执行完成后再根据匹配列表最终统计。经过测试发现利用八字批量预测仍然是随机概率，一点也没提高
        for pipei in tongji['匹配列表']:
            if len(pipei) == 1:
                tongji['匹配1'] += 1
            if len(pipei) == 2:
                tongji['匹配1'] += 1
                tongji['匹配2'] += 1
            if len(pipei) == 3:
                tongji['匹配1'] += 1
                tongji['匹配2'] += 1
                tongji['匹配3'] += 1
        tongji['概率1'] = tongji['匹配1'] / tongji['已执行']
        tongji['概率2'] = tongji['匹配2'] / tongji['已执行']
        tongji['概率3'] = tongji['匹配3'] / tongji['已执行']
        print(tongji)

    def test_qimen(self):
        fucai3d = self.db.get_tabledict_list("[体彩排列三]")
        tongji = {'已执行': 0, '匹配': 0, '概率': 0, '成本': 0, '盈利': 0, '匹配列表': []}

        def get_qushu(table_row0,last_num):
            dt_obj = datetime.datetime.strptime(table_row0, '%Y-%m-%d')
            dt_obj += datetime.timedelta(hours=20, minutes=30)
            qimen = QimenApi()
            qimen.paipan(dt_obj)
            res = qimen.get_cecaifenxi(last_num)
            print(res['测彩分析']['建议取数'])
            qushu_list = res['测彩分析']['建议投注']
            return qushu_list

        # 逐条解析历史数据，每一条都会调用一次预测功能
        for i,table_row in enumerate(fucai3d):
            if i == len(fucai3d)-2:
                break
            # if 2300<i<2350:
            if True:
                last_num = fucai3d[i+1]['中奖号码'].split(' ')
                print(table_row)
                print(last_num)
                qushu = get_qushu(table_row['开奖日期'],last_num)
                # print(qushu)
                print(len(qushu))
                pipei = []
                for item in qushu:
                    if [int(table_row['百位']),int(table_row['十位']),int(table_row['个位'])] == item:
                        pipei.append(item)
                print(pipei)
                # 记录数据
                tongji['成本'] += 2*len(qushu)
                tongji['匹配列表'].append(pipei)
                tongji['已执行'] += 1

        # 全部执行完成后再根据匹配列表最终统计。仍是随机概率，也许批量预测根本不可行
        for pipei in tongji['匹配列表']:
            if len(pipei)>=1:
                tongji['匹配'] += 1
        tongji['概率'] = tongji['匹配'] / tongji['已执行']
        tongji['盈利'] = tongji['匹配']*1040 - tongji['成本']
        print(tongji)
