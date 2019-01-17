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
        self._wangshuai()
        self._geju()
        self._yongshen()
        self._qushu()
        return self.pan

    def _wangshuai(self):
        pass

    def _geju(self):
        pass

    def _yongshen(self):
        pass

    def _qushu(self):
        pass

    def output_addition(self):
        map_str = ''
        return map_str


class Lianghuafenxi(Chuantongfenxi):
    def __init__(self):
        super(Lianghuafenxi, self).__init__()
        self.pan = None
        self.db = Db()
        self.db2cdata = Db2Cdata()

    def fenxi(self, pan):
        self.pan = pan
        self.pan['标签'] = '量化分析'
        self.pan['量化分析'] = {}
        self.pan['量化分析']['八字权重表'] = self.db.get_tabledict_dict("[八字-八字权重]")
        self.pan['量化分析']['旺衰权重表'] = self.db.get_tabledict_dict("[八字-旺衰权重]")
        self.pan['量化分析']['八字传统定格表'] = self.db.get_tabledict_dict("[八字-八字传统定格表]")
        # self.pan['量化分析']['八字量化取用表'] = self.db.get_tabledict_dict("[八字-八字量化取用表]")
        self.pan['量化分析']['五行'] = self.pan['五行']  # 存储五行（六亲）量化值
        self.pan['量化分析']['天干'] = self.pan['天干']  # 后面会把所有地支转化为天干，存储十神量化值
        self.pan['量化分析']['六亲'] = {}
        self.pan['量化分析']['十神'] = {}
        for wuxing in self.pan['量化分析']['五行']:
            self.pan['量化分析']['六亲'][self.pan['量化分析']['五行'][wuxing]['六亲']] = self.pan['量化分析']['五行'][wuxing]
        for tiangan in self.pan['量化分析']['天干']:
            self.pan['量化分析']['十神'][self.pan['量化分析']['天干'][tiangan]['十神']] = self.pan['量化分析']['天干'][tiangan]
        self.pan['量化分析']['旺衰'] = {}
        self.pan['量化分析']['八字格局'] = ''
        self.pan['量化分析']['格局序号'] = ''
        self.pan['量化分析']['取用格局'] = ''
        self.pan['量化分析']['八字喜忌'] = {}
        self.pan['量化分析']['建议取用'] = {}
        self.pan['量化分析']['建议取数'] = ''
        self._wangshuai()
        self._geju()
        self._yongshen()
        self._qushu()
        return self.pan

    def _wangshuai(self):
        # 此处采用新浪博客“留指爪”的方法，原文没有提及五行自身旺衰的变化，我认为需要添加此逻辑
        # 1.八字旺衰：初始化八字权重系数之天干
        for name in ['年干', '月干', '日干', '时干']:  # 配置四柱的天干权值
            for item in self.pan['量化分析']['八字权重表']:
                if name == self.pan['量化分析']['八字权重表'][item]['宫位']:
                    self.pan['八字单字'][name]['系数'] = 1.0 * float(self.pan['量化分析']['八字权重表'][item]['权重'])
        # 2.八字旺衰：初始化八字权重系数之地支（藏干）
        for name in ['年支', '月支', '日支', '时支']:  # 配置四柱的地支藏干权值
            for item in self.pan['量化分析']['八字权重表']:
                if name == self.pan['量化分析']['八字权重表'][item]['宫位']:
                    self.pan['八字单字'][name]['藏干']['藏干1系数'] = float(self.pan['八字单字'][name]['藏干']['藏干1系数']) * float(
                        self.pan['量化分析']['八字权重表'][item]['权重'])
                    self.pan['八字单字'][name]['藏干']['藏干2系数'] = float(self.pan['八字单字'][name]['藏干']['藏干2系数']) * float(
                        self.pan['量化分析']['八字权重表'][item]['权重'])
                    self.pan['八字单字'][name]['藏干']['藏干3系数'] = float(self.pan['八字单字'][name]['藏干']['藏干3系数']) * float(
                        self.pan['量化分析']['八字权重表'][item]['权重'])
        # 3.八字旺衰：初始化天干本来系数（初始化八字权重系数之后）
        for tiangan in self.pan['量化分析']['天干']:
            self.pan['量化分析']['天干'][tiangan]['权重'] = 0
            for name in ['年干', '月干', '日干', '时干']:  # 把四柱天干的系数更新到十神量化值
                if tiangan == self.pan['八字单字'][name]['宫主']:
                    self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['系数'])
        # 4.八字旺衰：地支藏干系数转化到天干系数
        for name in ['年支','月支','日支','时支']:  # 把四柱地支藏干的系数更新到十神量化值
            if self.pan['八字单字'][name]['藏干']['藏干1'] != '无':  # 地支藏干1
                for tiangan in self.pan['量化分析']['天干']:
                    if tiangan == self.pan['八字单字'][name]['藏干']['藏干1']:
                        self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['藏干']['藏干1系数'])
            if self.pan['八字单字'][name]['藏干']['藏干2'] != '无':  # 地支藏干2
                for tiangan in self.pan['量化分析']['天干']:
                    if tiangan == self.pan['八字单字'][name]['藏干']['藏干2']:
                        self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['藏干']['藏干2系数'])
            if self.pan['八字单字'][name]['藏干']['藏干3'] != '无':  # 地支藏干3
                for tiangan in self.pan['量化分析']['天干']:
                    if tiangan == self.pan['八字单字'][name]['藏干']['藏干3']:
                        self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['藏干']['藏干3系数'])
        # 5.八字旺衰：干支关系转化到天干系数
        for guanxi in self.pan['干支关系']:  # 根据干支关系化生的天干及其系数，更新到十神量化值
            for zuhe in self.pan['干支关系'][guanxi]:
                for tiangan in self.pan['量化分析']['天干']:
                    if self.pan['干支关系'][guanxi][zuhe].get('化', None):
                        if tiangan == self.pan['干支关系'][guanxi][zuhe]['化']:
                            self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['干支关系'][guanxi][zuhe]['化系数'])
                    if self.pan['干支关系'][guanxi][zuhe].get('化1', None):
                        if tiangan == self.pan['干支关系'][guanxi][zuhe]['化1']:
                            self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['干支关系'][guanxi][zuhe]['化1系数'])
                    if self.pan['干支关系'][guanxi][zuhe].get('化2', None):
                        if tiangan == self.pan['干支关系'][guanxi][zuhe]['化2']:
                            self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['干支关系'][guanxi][zuhe]['化2系数'])
        # 6.八字旺衰：旺衰权重系数转化到天干系数（依月支）
        for tiangan in self.pan['量化分析']['天干']:
            for item in self.pan['量化分析']['旺衰权重表']:
                if self.pan['量化分析']['天干'][tiangan]['旺衰'] == item:
                    self.pan['量化分析']['天干'][tiangan]['权重'] *= float(self.pan['量化分析']['旺衰权重表'][item]['权重'])
        # 7.八字旺衰：天干系数（十神权值）归一化
        sum = 0
        for tiangan in self.pan['量化分析']['天干']:
            sum += self.pan['量化分析']['天干'][tiangan]['权重']
        for tiangan in self.pan['量化分析']['天干']:
            self.pan['量化分析']['天干'][tiangan]['归一'] = self.pan['量化分析']['天干'][tiangan]['权重']/sum*100
        # 8.八字旺衰：六亲权重（天干十神的简单归并）
        for wuxing in self.pan['量化分析']['五行']:
            self.pan['量化分析']['五行'][wuxing]['权重'] = 0
            for tiangan in self.pan['量化分析']['天干']:
                if self.pan['量化分析']['天干'][tiangan]['五行'] == wuxing:
                    self.pan['量化分析']['五行'][wuxing]['权重'] += self.pan['量化分析']['天干'][tiangan]['权重']
            self.pan['量化分析']['五行'][wuxing]['归一'] = self.pan['量化分析']['五行'][wuxing]['权重']/sum*100
        # 1.日主旺衰：己生助
        self.pan['量化分析']['旺衰']['己生助'] = 0
        for wuxing in self.pan['量化分析']['五行']:
            if self.pan['量化分析']['五行'][wuxing]['六亲'] in ['比劫', '印枭']:
                self.pan['量化分析']['旺衰']['己生助'] += self.pan['量化分析']['五行'][wuxing]['归一']
        # 2.日主旺衰：克泄耗
        self.pan['量化分析']['旺衰']['克泄耗'] = 0
        for wuxing in self.pan['量化分析']['五行']:
            if self.pan['量化分析']['五行'][wuxing]['六亲'] in ['官杀', '财星', '食伤']:
                self.pan['量化分析']['旺衰']['克泄耗'] += self.pan['量化分析']['五行'][wuxing]['归一']
        # 3.日主旺衰：阴气
        self.pan['量化分析']['旺衰']['阴气'] = 0
        for tiangan in self.pan['量化分析']['天干']:
            if tiangan in ['乙', '丁', '己', '辛', '癸']:
                self.pan['量化分析']['旺衰']['阴气'] += self.pan['量化分析']['天干'][tiangan]['归一']
        # 4.日主旺衰：阳气
        self.pan['量化分析']['旺衰']['阳气'] = 0
        for tiangan in self.pan['量化分析']['天干']:
            if tiangan in ['甲', '丙', '戊', '庚', '壬']:
                self.pan['量化分析']['旺衰']['阳气'] += self.pan['量化分析']['天干'][tiangan]['归一']
        # 5.日主旺衰：分段判定。这里的百分比是很重要的参数
        self.pan['量化分析']['旺衰']['日干'] = '无'
        if self.pan['量化分析']['旺衰']['己生助'] < 17:
            self.pan['量化分析']['旺衰']['日干'] = '极弱'
        elif 17 < self.pan['量化分析']['旺衰']['己生助'] <= 37:
            self.pan['量化分析']['旺衰']['日干'] = '弱'
        elif 37 < self.pan['量化分析']['旺衰']['己生助'] <= 47:
            self.pan['量化分析']['旺衰']['日干'] = '偏弱'
        elif 47 < self.pan['量化分析']['旺衰']['己生助'] <= 53:
            self.pan['量化分析']['旺衰']['日干'] = '中'
        elif 53 < self.pan['量化分析']['旺衰']['己生助'] <= 63:
            self.pan['量化分析']['旺衰']['日干'] = '偏强'
        elif 63 < self.pan['量化分析']['旺衰']['己生助'] <= 83:
            self.pan['量化分析']['旺衰']['日干'] = '强'
        elif 83 < self.pan['量化分析']['旺衰']['己生助']:
            self.pan['量化分析']['旺衰']['日干'] = '极强'

    def _geju(self):
        # 八字格局
        for tiangan in self.pan['量化分析']['八字传统定格表']:
            if self.pan['八字单字']['日干']['宫主'] == tiangan:
                geju_str = self.pan['量化分析']['八字传统定格表'][tiangan][self.pan['八字单字']['月支']['宫主']]
                self.pan['量化分析']['八字格局'] = geju_str.split(' ')[0]
                self.pan['量化分析']['格局序号'] = geju_str.split(' ')[1]
                if len(geju_str.split(' ')) >= 3:
                    self.pan['量化分析']['八字格局'] += geju_str.split(' ')[2]
        # 取用格局
        if self.pan['量化分析']['旺衰']['日干'] == '极弱':
            self.pan['量化分析']['取用格局'] = '从弱'
        elif self.pan['量化分析']['旺衰']['日干'] == '极强':
            self.pan['量化分析']['取用格局'] = '从强'
        elif self.pan['量化分析']['旺衰']['日干'] == '中':
            self.pan['量化分析']['取用格局'] = '通关'
        else:
            self.pan['量化分析']['取用格局'] = '扶抑'

    def _yongshen(self):
        # 取用不能仅靠量化，需要分类：
        # 扶抑：
        # 日干弱多官杀，不能克制官杀，而应当泄掉官杀，所以取印枭
        # 日干弱多财星，需要比劫来帮身
        # 日干弱多食伤，需要印枭克制
        # 日干强多印枭，需要财星泄日干以及制印枭
        # 日干强多比劫，需要官杀
        # 从格：
        # 日干极强从强，极弱从弱
        # 通关：
        # 日干中和，多财印需要官杀通关，多印食需要比劫通关，多官比需要印枭通关
        # 调候：
        # 日干中和且不需要通关，木火性燥取金水，金水性寒取木火
        # 1.喜忌
        # 1.1.扶抑喜忌
        if self.pan['量化分析']['取用格局'] == '扶抑':
            # 1.1.1.日干弱（财官食必大于53）
            if self.pan['量化分析']['旺衰']['日干'] in ['弱', '偏弱']:
                if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['财星']['归一']\
                        or self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:  # 取印枭
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['官杀']
                    if self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['财星']
                    else:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['食伤']
                elif self.pan['量化分析']['六亲']['财星']['归一'] > self.pan['量化分析']['六亲']['官杀']['归一'] \
                        or self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:  # 取比劫
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['财星']
                    if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['官杀']
                    else:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['食伤']
                else:  # 取印枭
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['食伤']
                    if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['财星']['归一']:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['官杀']
                    else:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['财星']
            # 1.1.2.日干强（印比必大于53）
            elif self.pan['量化分析']['旺衰']['日干'] in ['强', '偏强']:
                if self.pan['量化分析']['六亲']['印枭']['归一'] >= self.pan['量化分析']['六亲']['比劫']['归一']:  # 取财星
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['财星']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['比劫']
                    if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['官杀']
                    else:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['食伤']
                else:  # 取官杀
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['官杀']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['比劫']
                    if self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['财星']
                    else:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['食伤']
        # 1.2.从格喜忌（与扶抑喜忌对应相反）
        elif self.pan['量化分析']['取用格局'] in ['从弱', '从强']:
            # 1.2.1.从弱喜克泄耗
            if self.pan['量化分析']['取用格局'] == '从弱':
                if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['财星']['归一'] \
                        or self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['官杀']
                    if self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['财星']
                    else:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['食伤']
                elif self.pan['量化分析']['六亲']['财星']['归一'] > self.pan['量化分析']['六亲']['官杀']['归一'] \
                        or self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['财星']
                    if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['官杀']
                    else:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['食伤']
                else:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['食伤']
                    if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['财星']['归一']:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['官杀']
                    else:
                        self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['财星']
            # 1.2.2.从强喜生助
            elif self.pan['量化分析']['取用格局'] == '从强':
                if self.pan['量化分析']['六亲']['印枭']['归一'] >= self.pan['量化分析']['六亲']['比劫']['归一']:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['财星']
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['比劫']
                    if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['官杀']
                    else:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['食伤']
                else:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['官杀']
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['比劫']
                    if self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['财星']
                    else:
                        self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['食伤']
        # 1.3.通关喜忌
        elif self.pan['量化分析']['旺衰']['日干'] == '中':
            if self.pan['量化分析']['六亲']['财星']['归一'] + self.pan['量化分析']['六亲']['印枭']['归一'] >= 53:  # 取官杀
                self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['官杀']
                self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['比劫']
                if self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['印枭']['归一']:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['财星']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['印枭']
                else:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['财星']
            elif self.pan['量化分析']['六亲']['印枭']['归一'] + self.pan['量化分析']['六亲']['食伤']['归一'] >= 53:  # 取比劫
                self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['比劫']
                self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['官杀']
                if self.pan['量化分析']['六亲']['印枭']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['印枭']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['食伤']
                else:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['食伤']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['印枭']
            elif self.pan['量化分析']['六亲']['官杀']['归一'] + self.pan['量化分析']['六亲']['比劫']['归一'] >= 53:  # 取印枭
                self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['六亲']['印枭']
                if self.pan['量化分析']['六亲']['财星']['归一'] >= self.pan['量化分析']['六亲']['食伤']['归一']:
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['财星']
                else:
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['六亲']['食伤']
                if self.pan['量化分析']['六亲']['官杀']['归一'] >= self.pan['量化分析']['六亲']['比劫']['归一']:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['官杀']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['比劫']
                else:
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['六亲']['比劫']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['六亲']['官杀']
            # 1.4.调候喜忌
            else:
                if self.pan['量化分析']['五行']['木']['归一'] + self.pan['量化分析']['五行']['火']['归一'] >= self.pan['量化分析']['五行']['金']['归一'] + self.pan['量化分析']['五行']['水']['归一']:  # 取水金
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['五行']['水']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['五行']['金']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['五行']['火']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['五行']['木']
                else:  # 取火木
                    self.pan['量化分析']['八字喜忌']['喜1'] = self.pan['量化分析']['五行']['火']
                    self.pan['量化分析']['八字喜忌']['喜2'] = self.pan['量化分析']['五行']['木']
                    self.pan['量化分析']['八字喜忌']['忌1'] = self.pan['量化分析']['五行']['水']
                    self.pan['量化分析']['八字喜忌']['忌2'] = self.pan['量化分析']['五行']['金']
        # 2.通过喜忌取用
        self.pan['量化分析']['建议取用'] = {'五行': self.pan['量化分析']['八字喜忌']['喜1']['五行'], '六亲': self.pan['量化分析']['八字喜忌']['喜1']['六亲']}
        tmp_list = []
        for tiangan in self.pan['量化分析']['天干']:
            if self.pan['量化分析']['建议取用']['五行'] == self.pan['量化分析']['天干'][tiangan]['五行']:
                tmp_list.append(self.pan['量化分析']['天干'][tiangan])
        if tmp_list[0]['归一'] >= tmp_list[1]['归一']:
            self.pan['量化分析']['建议取用']['天干'] = tmp_list[0]['天干']
            self.pan['量化分析']['建议取用']['十神'] = tmp_list[0]['十神']
        else:
            self.pan['量化分析']['建议取用']['天干'] = tmp_list[1]['天干']
            self.pan['量化分析']['建议取用']['十神'] = tmp_list[1]['十神']

    def _qushu(self):
        self.pan['量化分析']['建议取数'] = self.pan['量化分析']['五行'][self.pan['量化分析']['八字喜忌']['喜1']['五行']]['五行数']+self.pan['量化分析']['五行'][self.pan['量化分析']['八字喜忌']['喜2']['五行']]['五行数']

    def output_addition(self):
        map_str = ''
        map_str += '\n\n【量化分析】\n'
        map_str += '六亲力量：'
        for i in self.pan['量化分析']['五行']:
            map_str += str(self.pan['量化分析']['五行'][i]['六亲'])
            map_str += str(i)
            map_str += str(round(self.pan['量化分析']['五行'][i]['归一'],2))+'%'
            map_str += ';'
        map_str += '\n'
        map_str += '十神力量：'
        for i in self.pan['量化分析']['天干']:
            map_str += str(self.pan['量化分析']['天干'][i]['十神'])
            map_str += str(i)
            map_str += str(round(self.pan['量化分析']['天干'][i]['归一'],2))+'%'
            map_str += ';'
        map_str += '\n'
        map_str += '命主强弱：'
        map_str += '己生助'+str(round(self.pan['量化分析']['旺衰']['己生助'],2))+'%;'
        map_str += '克泄耗'+str(round(self.pan['量化分析']['旺衰']['克泄耗'],2))+'%;'
        map_str += '阴气'+str(round(self.pan['量化分析']['旺衰']['阴气'],2))+'%;'
        map_str += '阳气'+str(round(self.pan['量化分析']['旺衰']['阳气'],2))+'%;'
        map_str += '命主'+str(self.pan['量化分析']['旺衰']['日干'])+';'
        map_str += '\n'
        map_str += '八字格局：'
        map_str += str(self.pan['量化分析']['八字格局'])+'格;'
        map_str += '\n'
        map_str += '取用格局：'
        map_str += str(self.pan['量化分析']['取用格局']) + '格;'
        map_str += '\n'
        map_str += '八字喜忌：喜'+self.pan['量化分析']['八字喜忌']['喜1']['五行']+self.pan['量化分析']['八字喜忌']['喜2']['五行']+';忌'+self.pan['量化分析']['八字喜忌']['忌1']['五行']+self.pan['量化分析']['八字喜忌']['忌2']['五行']+';'
        map_str += '\n'
        map_str += '建议取用：'+self.pan['量化分析']['建议取用']['六亲']+self.pan['量化分析']['建议取用']['五行']+';'+self.pan['量化分析']['建议取用']['十神']+self.pan['量化分析']['建议取用']['天干']+';'
        map_str += '\n'
        map_str += '建议取数：'+self.pan['量化分析']['建议取数']+';'
        map_str += '\n'
        # # 测试
        # for k in self.pan['量化分析']:
        #     map_str += str(k)+': '
        #     map_str += str(self.pan['量化分析'][k])
        #     map_str += '\n\n'
        return map_str
