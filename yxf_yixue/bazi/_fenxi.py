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
        pan['标签'] = '传统分析'
        self.wangshuai()
        self.geju()
        self.yongshen()
        self.qushu()
        return self.pan

    def wangshuai(self):
        pass

    def geju(self):
        pass

    def yongshen(self):
        pass

    def qushu(self):
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
        self.pan['量化分析']['八字权重'] = self.db.get_tabledict_dict("[八字-八字权重]")
        self.pan['量化分析']['旺衰权重'] = self.db.get_tabledict_dict("[八字-旺衰权重]")
        self.pan['量化分析']['八字传统定格表'] = self.db.get_tabledict_dict("[八字-八字传统定格表]")
        # self.pan['量化分析']['八字量化取用表'] = self.db.get_tabledict_dict("[八字-八字量化取用表]")
        self.pan['量化分析']['五行'] = self.pan['五行']  # 存储五行（六亲）量化值
        self.pan['量化分析']['天干'] = self.pan['天干']  # 后面会把所有地支转化为天干，存储十神量化值
        self.wangshuai()
        self.geju()
        self.yongshen()
        self.qushu()
        return self.pan

    def wangshuai(self):
        # 此处采用新浪博客“留指爪”的方法，原文没有提及五行自身旺衰的变化，我认为需要添加此逻辑
        # 八字权重
        for name in ['年干', '月干', '日干', '时干']:  # 配置四柱的天干权值
            for item in self.pan['量化分析']['八字权重']:
                if name == self.pan['量化分析']['八字权重'][item]['宫位']:
                    self.pan['八字单字'][name]['系数'] = 1.0 * float(self.pan['量化分析']['八字权重'][item]['权重'])
        for name in ['年支', '月支', '日支', '时支']:  # 配置四柱的地支藏干权值
            for item in self.pan['量化分析']['八字权重']:
                if name == self.pan['量化分析']['八字权重'][item]['宫位']:
                    self.pan['八字单字'][name]['藏干']['藏干1系数'] = float(self.pan['八字单字'][name]['藏干']['藏干1系数']) * float(
                        self.pan['量化分析']['八字权重'][item]['权重'])
                    self.pan['八字单字'][name]['藏干']['藏干2系数'] = float(self.pan['八字单字'][name]['藏干']['藏干2系数']) * float(
                        self.pan['量化分析']['八字权重'][item]['权重'])
                    self.pan['八字单字'][name]['藏干']['藏干3系数'] = float(self.pan['八字单字'][name]['藏干']['藏干3系数']) * float(
                        self.pan['量化分析']['八字权重'][item]['权重'])
        # 天干系数+地支藏干系数
        for tiangan in self.pan['量化分析']['天干']:
            self.pan['量化分析']['天干'][tiangan]['权重'] = 0
            for name in ['年干', '月干', '日干', '时干']:  # 把四柱天干的系数更新到十神量化值
                if tiangan == self.pan['八字单字'][name]['宫主']:
                    self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['系数'])
        for name in ['年支','月支','日支','时支']:  # 把四柱地支藏干的系数更新到十神量化值
            if self.pan['八字单字'][name]['藏干']['藏干1'] != '无':
                for tiangan in self.pan['量化分析']['天干']:
                    if tiangan == self.pan['八字单字'][name]['藏干']['藏干1']:
                        self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['藏干']['藏干1系数'])
            if self.pan['八字单字'][name]['藏干']['藏干2'] != '无':
                for tiangan in self.pan['量化分析']['天干']:
                    if tiangan == self.pan['八字单字'][name]['藏干']['藏干2']:
                        self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['藏干']['藏干2系数'])
            if self.pan['八字单字'][name]['藏干']['藏干3'] != '无':
                for tiangan in self.pan['量化分析']['天干']:
                    if tiangan == self.pan['八字单字'][name]['藏干']['藏干3']:
                        self.pan['量化分析']['天干'][tiangan]['权重'] += float(self.pan['八字单字'][name]['藏干']['藏干3系数'])
            # 干支关系转化天干
            for guanxi in self.pan['干支关系']:  # 根据干支关系化生的天干及其系数，更新到十神量化值
                for hua in self.pan['干支关系'][guanxi]:
                    for tiangan in self.pan['量化分析']['天干']:
                        if self.pan['干支关系'][guanxi][hua].get('化', None):
                            if tiangan == self.pan['干支关系'][guanxi][hua]['化']:
                                self.pan['量化分析']['天干'][tiangan]['权重'] += float(
                                    self.pan['干支关系'][guanxi][hua]['化系数'])
        # 旺衰权重（依月支）
        for tiangan in self.pan['量化分析']['天干']:
            for item in self.pan['量化分析']['旺衰权重']:
                if self.pan['量化分析']['天干'][tiangan]['旺衰'] == item:
                    self.pan['量化分析']['天干'][tiangan]['权重'] *= float(self.pan['量化分析']['旺衰权重'][item]['权重'])
        # 十神权值归一化
        sum = 0
        for tiangan in self.pan['量化分析']['天干']:
            sum += self.pan['量化分析']['天干'][tiangan]['权重']
        for tiangan in self.pan['量化分析']['天干']:
            self.pan['量化分析']['天干'][tiangan]['归一'] = self.pan['量化分析']['天干'][tiangan]['权重']/sum*100
        # 六亲权重（十神的简单归并）
        for wuxing in self.pan['量化分析']['五行']:
            self.pan['量化分析']['五行'][wuxing]['权重'] = 0
            for tiangan in self.pan['量化分析']['天干']:
                if self.pan['量化分析']['天干'][tiangan]['五行'] == wuxing:
                    self.pan['量化分析']['五行'][wuxing]['权重'] += self.pan['量化分析']['天干'][tiangan]['权重']
            self.pan['量化分析']['五行'][wuxing]['归一'] = self.pan['量化分析']['五行'][wuxing]['权重']/sum*100
        # 正式开始记录旺衰
        self.pan['量化分析']['旺衰'] = {}
        # 己生助
        self.pan['量化分析']['旺衰']['己生助'] = 0
        for wuxing in self.pan['量化分析']['五行']:
            if self.pan['量化分析']['五行'][wuxing]['六亲'] in ['比劫', '印枭']:
                self.pan['量化分析']['旺衰']['己生助'] += self.pan['量化分析']['五行'][wuxing]['归一']
        # 克泄耗
        self.pan['量化分析']['旺衰']['克泄耗'] = 0
        for wuxing in self.pan['量化分析']['五行']:
            if self.pan['量化分析']['五行'][wuxing]['六亲'] in ['官杀', '财星', '食伤']:
                self.pan['量化分析']['旺衰']['克泄耗'] += self.pan['量化分析']['五行'][wuxing]['归一']
        # 阴气
        self.pan['量化分析']['旺衰']['阴气'] = 0
        for tiangan in self.pan['量化分析']['天干']:
            if tiangan in ['乙', '丁', '己', '辛', '癸']:
                self.pan['量化分析']['旺衰']['阴气'] += self.pan['量化分析']['天干'][tiangan]['归一']
        # 阳气
        self.pan['量化分析']['旺衰']['阳气'] = 0
        for tiangan in self.pan['量化分析']['天干']:
            if tiangan in ['甲', '丙', '戊', '庚', '壬']:
                self.pan['量化分析']['旺衰']['阳气'] += self.pan['量化分析']['天干'][tiangan]['归一']
        # 日主。这里的百分比是很重要的参数
        self.pan['量化分析']['旺衰']['日干'] = '无'
        if self.pan['量化分析']['旺衰']['己生助'] < 20:
            self.pan['量化分析']['旺衰']['日干'] = '极弱'
        elif 20 < self.pan['量化分析']['旺衰']['己生助'] <= 37:
            self.pan['量化分析']['旺衰']['日干'] = '弱'
        elif 37 < self.pan['量化分析']['旺衰']['己生助'] <= 47:
            self.pan['量化分析']['旺衰']['日干'] = '偏弱'
        elif 47 < self.pan['量化分析']['旺衰']['己生助'] <= 53:
            self.pan['量化分析']['旺衰']['日干'] = '中'
        elif 53 < self.pan['量化分析']['旺衰']['己生助'] <= 63:
            self.pan['量化分析']['旺衰']['日干'] = '偏强'
        elif 63 < self.pan['量化分析']['旺衰']['己生助'] <= 80:
            self.pan['量化分析']['旺衰']['日干'] = '强'
        elif 80 < self.pan['量化分析']['旺衰']['己生助']:
            self.pan['量化分析']['旺衰']['日干'] = '极强'
        # 取用格局
        if self.pan['量化分析']['旺衰']['日干'] == '极弱':
            self.pan['量化分析']['取用格局'] = '从弱'
        elif self.pan['量化分析']['旺衰']['日干'] == '极强':
            self.pan['量化分析']['取用格局'] = '从强'
        elif self.pan['量化分析']['旺衰']['日干'] == '中':
            self.pan['量化分析']['取用格局'] = '通关'
        else:
            self.pan['量化分析']['取用格局'] = '扶抑'

    def geju(self):
        self.pan['量化分析']['格局'] = ''
        for tiangan in self.pan['量化分析']['八字传统定格表']:
            if self.pan['八字单字']['日干']['宫主'] == tiangan:
                geju_str = self.pan['量化分析']['八字传统定格表'][tiangan][self.pan['八字单字']['月支']['宫主']]
                self.pan['量化分析']['格局'] = geju_str.split(' ')[0]
                self.pan['量化分析']['格局序号'] = geju_str.split(' ')[1]
                if len(geju_str.split(' ')) >= 3:
                    self.pan['量化分析']['格局'] += geju_str.split(' ')[2]

    def yongshen(self):
        # 取用不能仅靠量化，需要分类：
        # 日干弱多官杀，不能克制官杀，而应当泄掉官杀，所以取印枭
        # 日干弱多财星，需要比劫来帮身
        # 日干弱多食伤，需要印枭克制
        # 日干强多印枭，需要财星泄日干与制印枭
        # 日干强多比劫，需要官杀
        # 日干极强从强，极弱从弱
        # 日干中和，多财印需要官杀通关，多印食需要比劫通关，多官比需要印枭通关
        # 日干中和且不需要通关，木火性燥取金水，金水性寒取木火

        if self.pan['量化分析']['旺衰']['日干'] in ['弱', '偏弱']:
            pass
        elif self.pan['量化分析']['旺衰']['日干'] in ['强', '偏强']:
            pass
        elif self.pan['量化分析']['旺衰']['日干'] in ['极弱', '极强']:
            if self.pan['量化分析']['旺衰']['日干'] == '极弱':
                pass
            elif self.pan['量化分析']['旺衰']['日干'] == '极强':
                pass
        elif self.pan['量化分析']['旺衰']['日干'] == '中':
            pass

    def qushu(self):
        pass

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
        map_str += str(self.pan['量化分析']['格局'])+'格;'
        map_str += str(self.pan['量化分析']['取用格局'])+'格;'
        map_str += '\n'
        map_str += '八字喜忌：'
        map_str += '\n'
        map_str += '建议取用：'
        map_str += '\n'
        map_str += '建议取数：'
        map_str += '\n'
        # 测试
        map_str += str(self.pan['量化分析'])
        return map_str
