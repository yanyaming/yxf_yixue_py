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

    def output_addition(self):
        map_str = ''
        return map_str


class Cecaifenxi:
    def __init__(self):
        self.pan = None
        self.db = Db()
        self.db2cdata = Db2Cdata()
        self.tianganName = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split(' ')

    def fenxi(self, pan, shangqijianghao):
        self.pan = pan
        self.pan['标签'] = '测彩分析'
        self.pan['测彩分析'] = {}
        self.pan['测彩分析']['六十甲子表'] = self.db.get_tabledict_dict("[基础表-六十甲子]")
        self.pan['测彩分析']['六十甲子列表'] = self.db.get_tabledict_list("[基础表-六十甲子]")
        self.pan['测彩分析']['杀号公式表'] = {
            '甲': '戊 庚 辛'.split(' '),
            '乙': '戊 己 辛'.split(' '),
            '丙': '庚 壬 癸'.split(' '),
            '丁': '庚 辛 癸'.split(' '),
            '戊': '甲 乙 壬'.split(' '),
            '己': '乙 壬 癸'.split(' '),
            '庚': '甲 丙 丁'.split(' '),
            '辛': '甲 乙 丁'.split(' '),
            '壬': '丙 戊 己'.split(' '),
            '癸': '丙 丁 己'.split(' '),
        }
        self.pan['测彩分析']['纳数'] = {}
        self.pan['测彩分析']['建议取数'] = []
        self.pan['测彩分析']['建议投注'] = []
        self.pan['测彩分析']['投注信息'] = {}
        self._nashu()
        self._jiugongfeibo()
        self._feigongshahao(shangqijianghao)
        self._xuanhaotouzhu()
        return self.pan

    def _nashu(self):
        nianzhu_tmp = {}
        nashu_tmp = []
        num_tmp = 0
        for i in range(60):
            if self.pan['占时']['干支']['年柱'] == self.pan['测彩分析']['六十甲子列表'][i]['六十甲子']:
                nianzhu_tmp = {'干支': self.pan['占时']['干支']['年柱'], '序号': i}
        for i in range(10):
            if nianzhu_tmp['序号']-i >= 0:
                nashu_tmp.append(self.pan['测彩分析']['六十甲子列表'][nianzhu_tmp['序号']-i])
            else:
                nashu_tmp.append(self.pan['测彩分析']['六十甲子列表'][nianzhu_tmp['序号']-i+60])
        for i in nashu_tmp:
            num_tmp += 1
            if num_tmp == 10:
                num_tmp -= 10
            self.pan['测彩分析']['纳数'][num_tmp] = i['六十甲子']

    def _jiugongfeibo(self):
        # 六十甲子九宫飞泊规律：
        # 1.几局则甲子落在几宫，阳遁顺排，阴遁逆排，按照宫序排完六十甲子，共有18种局。
        # 2.每一节气的三元有关联，需要在本局之外补充整个三元三局的内容。
        for j in self.pan['盘'].keys():
            self.pan['盘'][j]['飞泊甲子'] = {'上元': [], '中元': [], '下元': []}
        # 三元局
        index1 = self.pan['信息']['三元补充']['上元']
        for i in self.pan['测彩分析']['六十甲子列表']:
            for j in self.pan['盘'].keys():
                if self.pan['盘'][j]['宫数'] == index1:
                    self.pan['盘'][j]['飞泊甲子']['上元'].append(i['六十甲子'])
            if self.pan['信息']['阴阳'] == '阳':
                index1 += 1
            else:
                index1 -= 1
            if index1 <= 0:
                index1 += 9
            if index1 >= 10:
                index1 -= 9
        index2 = self.pan['信息']['三元补充']['中元']
        for i in self.pan['测彩分析']['六十甲子列表']:
            for j in self.pan['盘'].keys():
                if self.pan['盘'][j]['宫数'] == index2:
                    self.pan['盘'][j]['飞泊甲子']['中元'].append(i['六十甲子'])
            if self.pan['信息']['阴阳'] == '阳':
                index2 += 1
            else:
                index2 -= 1
            if index2 <= 0:
                index2 += 9
            if index2 >= 10:
                index2 -= 9
        index3 = self.pan['信息']['三元补充']['下元']
        for i in self.pan['测彩分析']['六十甲子列表']:
            for j in self.pan['盘'].keys():
                if self.pan['盘'][j]['宫数'] == index3:
                    self.pan['盘'][j]['飞泊甲子']['下元'].append(i['六十甲子'])
            if self.pan['信息']['阴阳'] == '阳':
                index3 += 1
            else:
                index3 -= 1
            if index3 <= 0:
                index3 += 9
            if index3 >= 10:
                index3 -= 9

    def _feigongshahao(self, shangqijianghao):
        # 每一位单独分析
        for jianghao in shangqijianghao:
            # 待杀号码池
            set_tmp = set()
            for i in range(10):
                set_tmp.add(i)
            # 此号码的数据记录
            base_tmp = {}
            base_tmp['号码'] = int(jianghao)
            base_tmp['干支'] = self.pan['测彩分析']['纳数'][int(jianghao)]
            for i in self.pan['盘'].keys():
                if base_tmp['干支'] in self.pan['盘'][i]['飞泊甲子'][self.pan['信息']['三元']]:
                    base_tmp['落宫'] = {'宫数': self.pan['盘'][i]['宫数'], '地干': self.pan['盘'][i]['地干'], '天干': self.pan['盘'][i]['天干']}
            # 装甲防御（战车）：向下钻取一宫的地干（遇到戊己需要继续钻取）。
            for i in self.pan['盘'].keys():
                if self.pan['盘'][i]['天干'] == base_tmp['落宫']['地干']:
                    base_tmp['装甲防御'] = self.pan['盘'][i]['地干']
            if base_tmp['装甲防御'] in ['戊', '己']:
                for i in self.pan['盘'].keys():
                    if self.pan['盘'][i]['天干'] == base_tmp['装甲防御']:
                        base_tmp['装甲防御'] = self.pan['盘'][i]['地干']
            # 装甲攻击（火箭）：向上钻取一宫的天干（本宫天干乙直接使用合干庚，遇到戊己需要继续钻取，遇到回环需要酌情处理，以防御为主）。
            if base_tmp['落宫']['天干'] == '乙':
                base_tmp['装甲攻击'] = '庚'
            else:
                for i in self.pan['盘'].keys():
                    if self.pan['盘'][i]['地干'] == base_tmp['落宫']['天干']:
                        base_tmp['装甲攻击'] = self.pan['盘'][i]['天干']
                if base_tmp['装甲攻击'] in ['戊', '己']:
                    for i in self.pan['盘'].keys():
                        if self.pan['盘'][i]['地干'] == base_tmp['装甲攻击']:
                            base_tmp['装甲攻击'] = self.pan['盘'][i]['天干']
            # 空间防御（天军）：
            # 空间攻击（导弹）：
            # 统一杀号
            for i in self.pan['测彩分析']['杀号公式表'][base_tmp['装甲防御']]:
                for j in self.pan['测彩分析']['纳数'].keys():
                    if self.pan['测彩分析']['纳数'][j][0:1] == i:
                        set_tmp.discard(j)
            for i in self.pan['测彩分析']['杀号公式表'][base_tmp['装甲攻击']]:
                for j in self.pan['测彩分析']['纳数'].keys():
                    if self.pan['测彩分析']['纳数'][j][0:1] == i:
                        set_tmp.discard(j)
            base_tmp['暂定号码'] = set_tmp
            self.pan['测彩分析']['建议取数'].append(base_tmp['暂定号码'])
            # print(base_tmp)

    def _xuanhaotouzhu(self):
        for a in self.pan['测彩分析']['建议取数'][0]:
            for b in self.pan['测彩分析']['建议取数'][1]:
                for c in self.pan['测彩分析']['建议取数'][2]:
                    self.pan['测彩分析']['建议投注'].append([a,b,c])
        self.pan['测彩分析']['投注信息']['注数'] = len(self.pan['测彩分析']['建议投注'])
        self.pan['测彩分析']['投注信息']['成本'] = self.pan['测彩分析']['投注信息']['注数']*2

    def output_addition(self):
        map_str = ''
        map_str += '\n【测彩分析】\n'
        map_str += '建议取数：'+str(self.pan['测彩分析']['建议取数'])+'\n'
        map_str += '建议投注：'+str(self.pan['测彩分析']['建议投注'])+'\n'
        map_str += '注数：'+str(self.pan['测彩分析']['投注信息']['注数'])+'\n'
        map_str += '成本：'+str(self.pan['测彩分析']['投注信息']['成本'])+'\n'
        # 测试
        map_str += str(self.pan['测彩分析']['纳数'])+'\n'
        map_str += str(self.pan['占时'])+'\n'
        map_str += str(self.pan['信息'])+'\n'
        map_str += str(self.pan['盘'])+'\n'
        return map_str
