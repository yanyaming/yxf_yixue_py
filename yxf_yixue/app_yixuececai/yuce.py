import os
import datetime
from ..utils._db import Db
from ..bazi.bazi_api import BaziApi


class Yuce:
    def __init__(self):
        self.db = Db('app_yixuececai.db')

    def test_bazi(self):
        bazi = BaziApi()
        fucai3d = self.db.get_tabledict_list("[福彩3D]")
        for table_row in fucai3d:
            print(table_row)
            dt_obj = datetime.datetime.strptime(table_row['开奖日期'],'%Y-%m-%d')
            xingbie = '男'
            print(dt_obj)
            bazi.paipan(dt_obj, xingbie=xingbie)
            res = bazi.get_lianghuafenxi()
            print(res['量化分析']['建议取数'])
