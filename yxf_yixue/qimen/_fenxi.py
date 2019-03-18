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


class Cecaifenxi(Chuantongfenxi):
    def __init__(self):
        super(Cecaifenxi, self).__init__()
        self.pan = None
        self.db = Db()
        self.db2cdata = Db2Cdata()
        self.tianganName = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split(' ')

    def fenxi(self, pan):
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
        self.pan['测彩分析']['建议取数'] = {}
        self.pan['测彩分析']['建议投注'] = {}
        self._nashu()
        self._jiugongfeibo()
        self._feigongshahao()
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
            self.pan['测彩分析']['纳数'][i['天干']] = num_tmp

    def _jiugongfeibo(self):
        pass

    def _feigongshahao(self):
        pass

    def _xuanhaotouzhu(self):
        pass

    def output_addition(self):
        map_str = ''
        map_str += '\n【测彩分析】\n'
        map_str += '建议取数：'+str(self.pan['测彩分析']['建议取数'])+'\n'
        map_str += '建议投注：'+str(self.pan['测彩分析']['建议投注'])+'\n'
        # 测试
        map_str += str(self.pan['测彩分析']['纳数'])+'\n'
        map_str += str(self.pan['占时'])+'\n'
        map_str += str(self.pan['信息'])+'\n'
        map_str += str(self.pan['盘'])+'\n'
        return map_str
