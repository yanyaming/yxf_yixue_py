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

    def paipan(self, datetime_obj, calendar, solarTermJie, xingbie='男'):
        self.solar = calendar[0]
        self.lunar = calendar[1]
        self.solarTerm = calendar[2]
        self.solarTermJie = solarTermJie
        self.ganzhi = calendar[3]
        self.GZguanxi = {}
        self.Baziquanju = {}
        self.Bazisizhu = {'年柱': {'宫主': self.ganzhi.split('：')[1].split(' ')[0]},
                          '月柱': {'宫主': self.ganzhi.split('：')[1].split(' ')[1]},
                          '日柱': {'宫主': self.ganzhi.split('：')[1].split(' ')[2]},
                          '时柱': {'宫主': self.ganzhi.split('：')[1].split(' ')[3]}}
        self.Bazibazi = {'年干': {'宫主': self.ganzhi.split('：')[1].split(' ')[0][0:1]},
                         '年支': {'宫主': self.ganzhi.split('：')[1].split(' ')[0][1:2]},
                         '月干': {'宫主': self.ganzhi.split('：')[1].split(' ')[1][0:1]},
                         '月支': {'宫主': self.ganzhi.split('：')[1].split(' ')[1][1:2]},
                         '日干': {'宫主': self.ganzhi.split('：')[1].split(' ')[2][0:1]},
                         '日支': {'宫主': self.ganzhi.split('：')[1].split(' ')[2][1:2]},
                         '时干': {'宫主': self.ganzhi.split('：')[1].split(' ')[3][0:1]},
                         '时支': {'宫主': self.ganzhi.split('：')[1].split(' ')[3][1:2]}}
        self.Dayun = {}
        self.bazi()
        self.sizhu()
        self.shishen()
        self.dizhi_canggan()
        self.wuxing_wangshuai()
        self.rigan_shierzhangsheng()
        self.ganzhi_kongwang(self.ganzhi)
        self.ganzhi_guanxi()
        self.xingbie = xingbie
        self.dayun(datetime_obj, solarTermJie, xingbie)
        return {'干支':self.ganzhi,'五行':self.Wuxing, '天干':self.Tiangan, '地支':self.Dizhi, '八字全局':self.Baziquanju, '八字四柱':self.Bazisizhu, '八字单字':self.Bazibazi, '干支关系':self.GZguanxi, '大运':self.Dayun}

    def output(self):
        map_str = ''
        if self.xingbie == '男':
            map_str += '乾造：'
        else:
            map_str += '坤造：'
        map_str += self.ganzhi.split('：')[1]
        map_str += '\n'
        # 时间
        map_str += str(self.solar[1])
        map_str += '\n'
        map_str += str(self.lunar[1])
        map_str += '\n'
        # 节气
        map_str += '节气：'
        map_str += str(self.solarTermJie[0][0])
        map_str += '第'
        map_str += str(self.solarTermJie[0][2])
        map_str += '日\n\n'
        # 纳音
        map_str += self.Bazisizhu['年柱']['纳音五行']
        map_str += '\t\t'
        map_str += self.Bazisizhu['月柱']['纳音五行']
        map_str += '\t\t'
        map_str += self.Bazisizhu['日柱']['纳音五行']
        map_str += '\t\t'
        map_str += self.Bazisizhu['时柱']['纳音五行']
        map_str += '\n'
        # 天干十神
        map_str += self.Tiangan[self.Bazibazi['年干']['宫主']]['十神']
        map_str += '\t\t'
        map_str += self.Tiangan[self.Bazibazi['月干']['宫主']]['十神']
        map_str += '\t\t'
        map_str += '日干'
        map_str += '\t\t'
        map_str += self.Tiangan[self.Bazibazi['时干']['宫主']]['十神']
        map_str += '\t\t'
        map_str += '\n'
        # 天干
        map_str += self.Bazibazi['年干']['宫主']
        map_str += '\t\t'
        map_str += self.Bazibazi['月干']['宫主']
        map_str += '\t\t'
        map_str += self.Bazibazi['日干']['宫主']
        map_str += '\t\t'
        map_str += self.Bazibazi['时干']['宫主']
        map_str += '\n'
        # 地支
        map_str += self.Bazibazi['年支']['宫主']
        map_str += '\t\t'
        map_str += self.Bazibazi['月支']['宫主']
        map_str += '\t\t'
        map_str += self.Bazibazi['日支']['宫主']
        map_str += '\t\t'
        map_str += self.Bazibazi['时支']['宫主']
        map_str += '\n'
        # 地支藏干
        for i in range(1, 4):
            if self.Bazibazi['年支']['藏干']['藏干'+str(i)] != '无':
                map_str += self.Bazibazi['年支']['藏干']['藏干'+str(i)]
                map_str += self.Tiangan[self.Bazibazi['年支']['藏干']['藏干'+str(i)]]['十神']
            else:
                map_str += '      '
            map_str += '\t\t'
            if self.Bazibazi['月支']['藏干']['藏干'+str(i)] != '无':
                map_str += self.Bazibazi['月支']['藏干']['藏干'+str(i)]
                map_str += self.Tiangan[self.Bazibazi['月支']['藏干']['藏干'+str(i)]]['十神']
            else:
                map_str += '      '
            map_str += '\t\t'
            if self.Bazibazi['日支']['藏干']['藏干'+str(i)] != '无':
                map_str += self.Bazibazi['日支']['藏干']['藏干'+str(i)]
                map_str += self.Tiangan[self.Bazibazi['日支']['藏干']['藏干'+str(i)]]['十神']
            else:
                map_str += '      '
            map_str += '\t\t'
            if self.Bazibazi['时支']['藏干']['藏干'+str(i)] != '无':
                map_str += self.Bazibazi['时支']['藏干']['藏干'+str(i)]
                map_str += self.Tiangan[self.Bazibazi['时支']['藏干']['藏干'+str(i)]]['十神']
            else:
                map_str += '      '
            map_str += '\n'
        # 十二长生运
        shierzhangsheng = self.Bazibazi['日干']['十二长生'].copy()  # 改造变长字符串方便显示
        for item in shierzhangsheng.keys():
            if len(shierzhangsheng[item]) == 1:
                shierzhangsheng[item] += '  '
        map_str += shierzhangsheng[self.Bazibazi['年支']['宫主']]
        map_str += '\t\t'
        map_str += shierzhangsheng[self.Bazibazi['月支']['宫主']]
        map_str += '\t\t'
        map_str += shierzhangsheng[self.Bazibazi['日支']['宫主']]
        map_str += '\t\t'
        map_str += shierzhangsheng[self.Bazibazi['时支']['宫主']]
        map_str += '\n\n'
        # 干支关系
        for gx in self.GZguanxi.keys():
            map_str += gx
            map_str += '：'
            if self.GZguanxi[gx].keys():
                for k in self.GZguanxi[gx].keys():
                    map_str += k
            map_str += '\n'
        map_str += '\n'
        # 大运
        map_str += '大运：'
        map_str += '\n'
        for dayun in self.Dayun.keys():
            map_str += str(self.Dayun[dayun]['年份'])
            map_str += '\t\t'
        map_str += '\n'
        for dayun in self.Dayun.keys():
            map_str += str(self.Dayun[dayun]['虚岁'])
            map_str += '\t\t'
        map_str += '\n'
        for dayun in self.Dayun.keys():
            map_str += dayun
            map_str += '\t\t'
        map_str += '\n'
        for dayun in self.Dayun.keys():
            map_str += self.Dayun[dayun]['十神']
            map_str += '\t\t'
        map_str += '\n'
        for dayun in self.Dayun.keys():
            map_str += self.Dayun[dayun]['纳音五行']
            map_str += '\t\t'
        map_str += '\n'
        for dayun in self.Dayun.keys():
            if len(self.Dayun[dayun]['十二长生']) == 1:
                self.Dayun[dayun]['十二长生'] += '  '
            map_str += self.Dayun[dayun]['十二长生']
            map_str += '\t\t'
        print(map_str)

    def bazi(self):
        # 胎元：天干为月干+1，地支为月支+3
        taiyuan_tianganidx = self.tianganName.index(self.Bazibazi['月干']['宫主']) + 1
        if taiyuan_tianganidx >= 10:
            taiyuan_tianganidx -= 10
        taiyuan_dizhiidx = self.dizhiName.index(self.Bazibazi['月支']['宫主']) + 3
        if taiyuan_dizhiidx >= 12:
            taiyuan_dizhiidx -= 12
        self.Baziquanju['胎元'] = self.tianganName[taiyuan_tianganidx] + self.dizhiName[taiyuan_dizhiidx]
        # 命宫：地支子上起寅月逆数至生月，再起生时顺数至卯；若命宫地支在生月前则天干起甲逆数到命宫地支，否则顺数到命宫地支
        self.Baziquanju['命宫'] = None
        # 身宫：
        self.Baziquanju['身宫'] = None
        # 命卦：以出生时间起六爻卦，只取卦名
        self.Baziquanju['命卦'] = None

    def sizhu(self):
        for zhu in self.Bazisizhu.keys():
            self.Bazisizhu[zhu]['纳音五行'] = self.Liushijiazi[self.Bazisizhu[zhu]['宫主']]['纳音五行']

    def shishen(self):
        rigan = self.Bazibazi['日干']['宫主']
        riganwuxing = self.Tiangan[rigan]['五行']
        riganyinyang = self.Tiangan[rigan]['阴阳']
        # 五行生克关系
        caixing = self.db2cdata.get_wuxing_shengke(riganwuxing, return_type='耗')
        guansha = self.db2cdata.get_wuxing_shengke(riganwuxing, return_type='克')
        yinxiao = self.db2cdata.get_wuxing_shengke(riganwuxing, return_type='生')
        bijie = riganwuxing
        shishang = self.db2cdata.get_wuxing_shengke(riganwuxing, return_type='泄')
        # 五行六亲
        self.Wuxing[caixing]['六亲'] = '财星'
        self.Wuxing[guansha]['六亲'] = '官杀'
        self.Wuxing[yinxiao]['六亲'] = '印枭'
        self.Wuxing[bijie]['六亲'] = '比劫'
        self.Wuxing[shishang]['六亲'] = '食伤'
        # 天干十神
        for i in self.Tiangan.keys():
            if self.Tiangan[i]['五行'] == caixing:
                if self.Tiangan[i]['阴阳'] == riganyinyang:
                    self.Tiangan[i]['十神'] = '偏财'
                else:
                    self.Tiangan[i]['十神'] = '正财'
            if self.Tiangan[i]['五行'] == guansha:
                if self.Tiangan[i]['阴阳'] == riganyinyang:
                    self.Tiangan[i]['十神'] = '七杀'
                else:
                    self.Tiangan[i]['十神'] = '正官'
            if self.Tiangan[i]['五行'] == yinxiao:
                if self.Tiangan[i]['阴阳'] == riganyinyang:
                    self.Tiangan[i]['十神'] = '偏印'
                else:
                    self.Tiangan[i]['十神'] = '正印'
            if self.Tiangan[i]['五行'] == bijie:
                if self.Tiangan[i]['阴阳'] == riganyinyang:
                    self.Tiangan[i]['十神'] = '比肩'
                else:
                    self.Tiangan[i]['十神'] = '劫财'
            if self.Tiangan[i]['五行'] == shishang:
                if self.Tiangan[i]['阴阳'] == riganyinyang:
                    self.Tiangan[i]['十神'] = '食神'
                else:
                    self.Tiangan[i]['十神'] = '伤官'
        # 地支十神
        for i in self.Dizhi.keys():
            if self.Dizhi[i]['五行'] == caixing:
                if self.Dizhi[i]['阴阳'] == riganyinyang:
                    self.Dizhi[i]['十神'] = '偏财'
                else:
                    self.Dizhi[i]['十神'] = '正财'
            if self.Dizhi[i]['五行'] == guansha:
                if self.Dizhi[i]['阴阳'] == riganyinyang:
                    self.Dizhi[i]['十神'] = '七杀'
                else:
                    self.Dizhi[i]['十神'] = '正官'
            if self.Dizhi[i]['五行'] == yinxiao:
                if self.Dizhi[i]['阴阳'] == riganyinyang:
                    self.Dizhi[i]['十神'] = '偏印'
                else:
                    self.Dizhi[i]['十神'] = '正印'
            if self.Dizhi[i]['五行'] == bijie:
                if self.Dizhi[i]['阴阳'] == riganyinyang:
                    self.Dizhi[i]['十神'] = '比肩'
                else:
                    self.Dizhi[i]['十神'] = '劫财'
            if self.Dizhi[i]['五行'] == shishang:
                if self.Dizhi[i]['阴阳'] == riganyinyang:
                    self.Dizhi[i]['十神'] = '食神'
                else:
                    self.Dizhi[i]['十神'] = '伤官'

    def dizhi_canggan(self):
        table = self.db.get_tabledict_dict('[关联表-地支藏干]')
        for dizhi in [self.Bazibazi['年支'], self.Bazibazi['月支'], self.Bazibazi['日支'], self.Bazibazi['时支']]:
            dizhi['藏干'] = {}
            dizhi['藏干']['藏干1'] = table[dizhi['宫主']]['藏干1']
            dizhi['藏干']['藏干1系数'] = table[dizhi['宫主']]['藏干1系数']
            dizhi['藏干']['藏干2'] = table[dizhi['宫主']]['藏干2']
            dizhi['藏干']['藏干2系数'] = table[dizhi['宫主']]['藏干2系数']
            dizhi['藏干']['藏干3'] = table[dizhi['宫主']]['藏干3']
            dizhi['藏干']['藏干3系数'] = table[dizhi['宫主']]['藏干3系数']

    def wuxing_wangshuai(self):
        table = self.db.get_tabledict_dict('[关联表-五行旺衰]')
        self.Wuxing['木']['旺衰'] = table['木'][self.Bazibazi['月支']['宫主']]
        self.Wuxing['火']['旺衰'] = table['火'][self.Bazibazi['月支']['宫主']]
        self.Wuxing['土']['旺衰'] = table['土'][self.Bazibazi['月支']['宫主']]
        self.Wuxing['金']['旺衰'] = table['金'][self.Bazibazi['月支']['宫主']]
        self.Wuxing['水']['旺衰'] = table['水'][self.Bazibazi['月支']['宫主']]

    def rigan_shierzhangsheng(self):
        table = self.db.get_tabledict_dict('[关联表-天干十二长生运]')
        self.Bazibazi['日干']['十二长生'] = table[self.Bazibazi['日干']['宫主']]
        self.Bazibazi['日干']['十二长生'].pop('序号')
        self.Bazibazi['日干']['十二长生'].pop('天干')
        self.Bazibazi['日干']['十二长生'].pop('五行')
        self.Bazibazi['日干']['十二长生'].pop('阴阳')

    def ganzhi_kongwang(self, ganzhi):
        kongwang_str = ganzhi.split('：')[1].split('（')[1].split(' ')[2]
        self.Bazibazi['日干']['空亡'] = kongwang_str

    def ganzhi_guanxi(self):
        # 天干合化：日干不参与合化，天干最多只能出现1次五合（3干参与）。
        table_hehua = self.db.get_tabledict_dict('[关联表-天干五合]')
        self.GZguanxi['天干五合'] = {}
        for i in table_hehua.values():
            if i['天干1'] in [self.Bazibazi['年干']['宫主'], self.Bazibazi['月干']['宫主'], self.Bazibazi['时干']['宫主']] and i['天干2'] in [self.Bazibazi['年干']['宫主'], self.Bazibazi['月干']['宫主'], self.Bazibazi['时干']['宫主']]:
                self.GZguanxi['天干五合'][i['天干1'] + i['天干2']] = {}
                self.GZguanxi['天干五合'][i['天干1'] + i['天干2']]['化'] = i['合化天干']
                self.GZguanxi['天干五合'][i['天干1'] + i['天干2']]['化系数'] = '1.0'
        # 地支关系优先级：
        # 地支关系中，同类关系可能存在多个。
        # 地支六冲：有冲得与冲去之分，反映在系数里，系数为负即为冲去。
        table_liuchong = self.db.get_tabledict_dict('[关联表-地支六冲]')
        self.GZguanxi['地支六冲'] = {}
        for i in table_liuchong.values():
            if i['地支1'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] and i['地支2'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']]:
                self.GZguanxi['地支六冲'][i['地支1'] + i['地支2']] = {}
                self.GZguanxi['地支六冲'][i['地支1'] + i['地支2']]['化'] = i['冲化天干']
                self.GZguanxi['地支六冲'][i['地支1'] + i['地支2']]['化系数'] = i['系数']
        # 地支六合：
        table_liuhe = self.db.get_tabledict_dict('[关联表-地支六合]')
        self.GZguanxi['地支六合'] = {}
        for i in table_liuhe.values():
            if i['地支1'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] and i['地支2'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']]:
                self.GZguanxi['地支六合'][i['地支1'] + i['地支2']] = {}
                self.GZguanxi['地支六合'][i['地支1'] + i['地支2']]['化'] = i['合化天干']
                self.GZguanxi['地支六合'][i['地支1'] + i['地支2']]['化系数'] = '1.0'
        # 地支三会：
        table_sanhui = self.db.get_tabledict_dict('[关联表-地支三会]')
        self.GZguanxi['地支三会'] = {}
        for i in table_sanhui.values():
            if i['地支1'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] \
                    and i['地支2'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] \
                    and i['地支3'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']]:
                self.GZguanxi['地支三会'][i['地支1'] + i['地支2'] + i['地支3']] = {}
                self.GZguanxi['地支三会'][i['地支1'] + i['地支2'] + i['地支3']]['化1'] = i['合会天干1']
                self.GZguanxi['地支三会'][i['地支1'] + i['地支2'] + i['地支3']]['化1系数'] = i['合会天干1系数']
                self.GZguanxi['地支三会'][i['地支1'] + i['地支2'] + i['地支3']]['化2'] = i['合会天干2']
                self.GZguanxi['地支三会'][i['地支1'] + i['地支2'] + i['地支3']]['化2系数'] = i['合会天干2系数']
        # 地支三合：优先考察三合，若没有三合再看半合
        table_sanhe = self.db.get_tabledict_dict('[关联表-地支三合]')
        self.GZguanxi['地支三合'] = {}
        self.GZguanxi['地支生半合'] = {}
        self.GZguanxi['地支墓半合'] = {}
        for i in table_sanhe.values():
            if i['地支1'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] \
                    and i['地支2'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] \
                    and i['地支3'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']]:
                self.GZguanxi['地支三合'][i['地支1'] + i['地支2'] + i['地支3']] = {}
                self.GZguanxi['地支三合'][i['地支1'] + i['地支2'] + i['地支3']]['化'] = i['合化天干']
                self.GZguanxi['地支三合'][i['地支1'] + i['地支2'] + i['地支3']]['化系数'] = '1.0'
            else:
                # 地支生半合：
                if i['地支1'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] \
                        and i['地支2'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']]:
                    self.GZguanxi['地支生半合'][i['地支1'] + i['地支2']] = {}
                    self.GZguanxi['地支生半合'][i['地支1'] + i['地支2']]['化'] = i['合化天干']
                    self.GZguanxi['地支生半合'][i['地支1'] + i['地支2']]['化系数'] = '0.5'
                # 地支墓半合：
                if i['地支2'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']] \
                        and i['地支3'] in [self.Bazibazi['年支']['宫主'], self.Bazibazi['月支']['宫主'], self.Bazibazi['日支']['宫主'], self.Bazibazi['时支']['宫主']]:
                    self.GZguanxi['地支墓半合'][i['地支2'] + i['地支3']] = {}
                    self.GZguanxi['地支墓半合'][i['地支2'] + i['地支3']]['化'] = i['合化天干']
                    self.GZguanxi['地支墓半合'][i['地支2'] + i['地支3']]['化系数'] = '0.5'
        # 刑破害为定性分析，暂时不需要定量。
        # 三刑
        # 六破
        # 六害

    def dayun(self, dt, solarTermJie, xingbie):
        # 确定大运。从所生之月建依次按顺逆序得出。男年干阳、女年干阴顺行；男年干阴、女年干阳逆行。
        yuejian = self.Bazisizhu['月柱']['宫主']
        yuejianIdx = int(self.Liushijiazi[yuejian]['序号'])
        niangan = self.Bazibazi['年干']['宫主']
        if (xingbie == '男' and niangan in '甲 丙 戊 庚 壬'.split(' ')) or (xingbie == 0 and niangan in '乙 丁 己 辛 癸'.split(' ')):
            shunni = '顺'
        else:
            shunni = '逆'
        if shunni == '顺':
            for j in range(1, 11):
                idx = yuejianIdx + j
                if idx > 60:
                    idx -= 60
                for i in self.Liushijiazi.keys():
                    if int(self.Liushijiazi[i]['序号']) == idx:
                        self.Dayun[i] = {}
        else:
            for j in range(1, 11):
                idx = yuejianIdx - j
                if idx < 1:
                    idx += 60
                for i in self.Liushijiazi.keys():
                    if int(self.Liushijiazi[i]['序号']) == idx:
                        self.Dayun[i] = {}
        # 上一个节与下一个节的日期
        jiedate1 = solarTermJie[0][1]
        jiedate2 = solarTermJie[1][1]
        # 起运年数。大运顺行则由生日生时顺数到下一节，大运逆行则由生日生时逆数到上一节。每隔三日一岁，每隔一日120天，因节气没有精确到时辰，所以交运只精确到一年。
        if shunni == '顺':
            dayIdx = (jiedate2 - dt).days
        else:
            dayIdx = (dt - jiedate1).days
        qiyunzhousui = round(dayIdx/3)  # 周岁
        for i, item in enumerate(self.Dayun):
            self.Dayun[item]['十神'] = self.Tiangan[item[0:1]]['十神']
            self.Dayun[item]['十二长生'] = self.Bazibazi['日干']['十二长生'][item[1:2]]
            self.Dayun[item]['纳音五行'] = self.Liushijiazi[item]['纳音五行']
            self.Dayun[item]['虚岁'] = qiyunzhousui + i*10 + 1  # 虚岁
            self.Dayun[item]['年份'] = dt.year + qiyunzhousui + i*10
