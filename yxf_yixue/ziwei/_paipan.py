#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db, Db2Cdata


class Paipan:
    def __init__(self):
        self.wuxingName = '木 火 土 金 水'.split(' ')
        self.tianganName = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split(' ')
        self.dizhiName = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')
        # 导入数据
        self.db = Db()
        self.db2cdata = Db2Cdata()
        self.Wuxing = self.db.get_tabledict_dict("[基础表-五行]")
        self.Tiangan = self.db.get_tabledict_dict("[基础表-十天干]")
        self.Dizhi = self.db.get_tabledict_dict("[基础表-十二地支]")
        self.Bagua = self.db.get_tabledict_dict("[基础表-八卦]")
        self.Liushisigua = self.db.get_tabledict_dict("[基础表-六十四卦]")
        self.Liushijiazi = self.db.get_tabledict_dict("[基础表-六十甲子]")
        self.Luoshu = self.db.get_tabledict_dict("[基础表-洛书九宫格]")

    def paipan(self, datetime_obj, calendar, solarTermJie, xingbie):
        pass

    def output(self):
        pass