#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.db import Db
from utils.db2cdata import Db2Cdata


class Fenxi:
    def __init__(self):
        pass

    class Chuantongfenxi:
        def __init__(self):
            self.db = Db()
            self.db2cdata = Db2Cdata()
            self.Wuxing = self.db.get_tabledict_dict("[基础表-五行]")
            self.Tiangan = self.db.get_tabledict_dict("[基础表-十天干]")
            self.Dizhi = self.db.get_tabledict_dict("[基础表-十二地支]")
            self.Bagua = self.db.get_tabledict_dict("[基础表-八卦]")
            self.Liushisigua = self.db.get_tabledict_dict("[基础表-六十四卦]")
            self.Liushijiazi = self.db.get_tabledict_dict("[基础表-六十甲子]")
            self.Luoshu = self.db.get_tabledict_dict("[基础表-洛书九宫格]")

        def fenxi(self, ganzhi, Info, Pan):
            self.ganzhi = ganzhi
            self.Info = Info
            self.Pan = Pan

    class CecaiFenxi:
        # 返回数字或数位
        def __init__(self):
            self.dizhiName = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')

        def cecaifenxi(self, dt, Info, Pan):
            self.dt = dt
            self.Info = Info
            self.Pan = Pan

        def danqishikongfa(self, qiguashuru):
            # 先排盘：时间起卦+输入开奖号对应的动爻
            dongyao = qiguashuru  # 动爻数字
            shu1 = self.dizhiName.index(self.Pan['1' + str(dongyao)]['纳支']) + 1
            shu2 = self.dizhiName.index(self.Pan['2' + str(dongyao)]['纳支']) + 1
            if shu1 >= 10:
                shu1 -= 10
            if shu2 >= 10:
                shu2 -= 10
            # 次日日支
            rizhi = self.dt[1].split('：')[1].split(' ')[2][1:2]
            shu3 = self.dizhiName.index(rizhi) + 1
            if shu3 >= 10:
                shu3 -= 10
            return [shu1, shu2, shu3]

        def chunshijianguafa(self):
            # 先排盘：时间起卦+输入开奖号对应的动爻
            dongyao = 0  # 动爻数字
            shu1 = self.dizhiName.index(self.Pan['1' + str(dongyao)]['纳支']) + 1
            shu2 = self.dizhiName.index(self.Pan['2' + str(dongyao)]['纳支']) + 1
            if shu1 >= 10:
                shu1 -= 10
            if shu2 >= 10:
                shu2 -= 10
            # 次日日支
            rizhi = self.dt[1].split('：')[1].split(' ')[2][1:2]
            shu3 = self.dizhiName.index(rizhi) + 1
            if shu3 >= 10:
                shu3 -= 10
            return [shu1, shu2, shu3]
