#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db, Db2Cdata


class Paipan:
    def __init__(self):
        # 初始数据
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

    def paipan(self, datetime_obj, calendar):
        # 排盘争议1：转盘（布局按照旋转顺序），飞盘（布局按照宫数顺序），选择转盘。
        # 排盘争议2：拆补（上元天数可调整，多退少补），置闰（三元固定天数，逐渐积累到一个节气的天数就置闰），选择拆补。
        # 排盘尺度：时家奇门兼刻家奇门。
        self.solar = calendar[0]
        self.lunar = calendar[1]
        self.solarTerm = calendar[2]
        self.ganzhi = calendar[3]
        self.Xinxi = {'三元': '', '阴阳': '', '遁局': '', '月将': '', '旬首': '', '值符': '', '值使': ''}
        self.Pan = {}
        self.Res = {}
        return self.Res

    def _xinxi(self):
        pass

    def _dipan(self):
        pass

    def _tianpan(self):
        pass

    def _bamen(self):
        pass

    def _jiuxing(self):
        pass

    def _bashen(self):
        pass

    def output(self):
        map_str = ''
        return map_str
