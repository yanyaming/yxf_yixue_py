#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db, Db2Cdata


class Chuantongfenxi:
    def __init__(self):
        self.pan = None
        self.db = Db()
        self.db2cdata = Db2Cdata()

    def fenxi(self, pan):
        self.pan = pan
        self.pan['标签'] = '传统分析'
        return self.pan


class Cecaifenxi(Chuantongfenxi):
    def __init__(self):
        super(Cecaifenxi, self).__init__()
        self.pan = None
        self.db = Db()
        self.db2cdata = Db2Cdata()

    def fenxi(self, pan):
        self.pan = pan
        self.pan['标签'] = '测彩分析'
        return self.pan

    # def danqishikongfa(self, qiguashuru):
    #     # 先排盘：时间起卦+输入开奖号对应的动爻
    #     dongyao = qiguashuru  # 动爻数字
    #     shu1 = self.dizhiName.index(self.Pan['1' + str(dongyao)]['纳支']) + 1
    #     shu2 = self.dizhiName.index(self.Pan['2' + str(dongyao)]['纳支']) + 1
    #     if shu1 >= 10:
    #         shu1 -= 10
    #     if shu2 >= 10:
    #         shu2 -= 10
    #     # 次日日支
    #     rizhi = self.dt[1].split('：')[1].split(' ')[2][1:2]
    #     shu3 = self.dizhiName.index(rizhi) + 1
    #     if shu3 >= 10:
    #         shu3 -= 10
    #     return [shu1, shu2, shu3]
    #
    # def chunshijianguafa(self):
    #     # 先排盘：时间起卦+输入开奖号对应的动爻
    #     dongyao = 0  # 动爻数字
    #     shu1 = self.dizhiName.index(self.Pan['1' + str(dongyao)]['纳支']) + 1
    #     shu2 = self.dizhiName.index(self.Pan['2' + str(dongyao)]['纳支']) + 1
    #     if shu1 >= 10:
    #         shu1 -= 10
    #     if shu2 >= 10:
    #         shu2 -= 10
    #     # 次日日支
    #     rizhi = self.dt[1].split('：')[1].split(' ')[2][1:2]
    #     shu3 = self.dizhiName.index(rizhi) + 1
    #     if shu3 >= 10:
    #         shu3 -= 10
    #     return [shu1, shu2, shu3]
