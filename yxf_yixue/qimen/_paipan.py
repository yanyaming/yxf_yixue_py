#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db, Db2Cdata


class Paipan:
    def __init__(self):
        # 初始数据
        self.wuxingName = '木 火 土 金 水'.split(' ')
        self.tianganName = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split(' ')
        self.dizhiName = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')
        self.sanqiliuyiName = '戊 己 庚 辛 壬 癸 丁 丙 乙'.split(' ')
        # 导入数据
        self.db = Db()
        self.db2cdata = Db2Cdata()
        self.Wuxing = self.db.get_tabledict_dict("[基础表-五行]")
        self.Tiangan = self.db.get_tabledict_dict("[基础表-十天干]")
        self.Dizhi = self.db.get_tabledict_dict("[基础表-十二地支]")
        self.Liushijiazi = self.db.get_tabledict_dict("[基础表-六十甲子]")
        self.Liushijiazilist = self.db.get_tabledict_list("[基础表-六十甲子]")
        self.Bagua = self.db.get_tabledict_dict("[基础表-八卦]")
        self.Luoshu = self.db.get_tabledict_dict("[基础表-洛书九宫格]")
        self.Qimentiangan = self.db.get_tabledict_dict("[三式-奇门天干]")
        self.Qimenbamen = self.db.get_tabledict_dict("[三式-奇门八门]")
        self.Qimenjiuxing = self.db.get_tabledict_dict("[三式-奇门九星]")
        self.Qimenbashen = self.db.get_tabledict_dict("[三式-奇门八神]")

    def paipan(self, datetime_obj, calendar, bujufangfa):
        # 排盘争议1：转盘（排宫，布局按照旋转顺序），飞盘（飞宫，布局按照宫数顺序），通过输入选择。
        # 排盘争议2：拆补（上元天数可调整，多退少补），置闰（三元固定天数，逐渐积累到一个节气的天数就置闰），选择拆补。
        # 排盘争议3：布三奇六仪，南炎子的例子与书上理论相同没问题，玄奥软件和主流在线排盘反而都错了。
        # 排盘尺度：时家奇门兼刻家奇门。
        self.solar = calendar[0]
        self.lunar = calendar[1]
        self.solarTerm = calendar[2]
        self.ganzhi = calendar[3]
        self.Xinxi = {'节气': self.solarTerm['节气名称'], '月将': self.solarTerm['文本'][-5:-4], '阴阳': '', '三元': '', '遁局': '', '旬首': '', '值符': '', '值使': '', '布局方法': bujufangfa}
        self.Pan = {'1': {'宫数': 4, '转数': 5, '宫卦': '巽', '宫五行': '木', '宫支': '辰巳', '宫门': '杜', '宫星': '辅'}, '2': {'宫数': 9, '转数': 6, '宫卦': '离', '宫五行': '火', '宫支': '午', '宫门': '景', '宫星': '英'}, '3': {'宫数': 2, '转数': 7, '宫卦': '坤', '宫五行': '土', '宫支': '未申', '宫门': '死', '宫星': '芮'},
                    '4': {'宫数': 3, '转数': 4, '宫卦': '震', '宫五行': '木', '宫支': '卯', '宫门': '伤', '宫星': '冲'}, '5': {'宫数': 5, '转数': 9, '宫卦': '中', '宫五行': '土', '宫支': '', '宫门': '中', '宫星': '禽'}, '6': {'宫数': 7, '转数': 8, '宫卦': '兑', '宫五行': '金', '宫支': '酉', '宫门': '惊', '宫星': '柱'},
                    '7': {'宫数': 8, '转数': 3, '宫卦': '艮', '宫五行': '土', '宫支': '丑寅', '宫门': '生', '宫星': '任'}, '8': {'宫数': 1, '转数': 2, '宫卦': '坎', '宫五行': '水', '宫支': '子', '宫门': '休', '宫星': '蓬'}, '9': {'宫数': 6, '转数': 1, '宫卦': '乾', '宫五行': '金', '宫支': '戌亥', '宫门': '开', '宫星': '心'}}
        self._xinxi()
        self._dipan()
        self._tianpan(bujufangfa)
        self._renpan()
        self._shenpan()
        self.Res = {'占时': {'节气': self.solarTerm, '干支': self.ganzhi}, '信息': self.Xinxi, '盘': self.Pan}
        return self.Res

    def _xinxi(self):
        # 阴阳遁：夏至12到冬至24为阴遁，冬至24到夏至12为阳遁
        if 12 <= self.solarTerm['节气序号'] < 24:
            self.Xinxi['阴阳'] = '阴'
        else:
            self.Xinxi['阴阳'] = '阳'
        # 三元：当日干支往前推，推到甲日或己日，看其地支，子午卯酉为上元，寅申巳亥为中元，辰戌丑未为下元
        rizhu_tmp = None
        for i in range(60):
            if self.ganzhi['日柱'] == self.Liushijiazilist[i]['六十甲子']:
                rizhu_tmp = {'干支': self.ganzhi['日柱'], '序号': i}  # 得到当日甲子及其在表中的序号
        for i in range(5):  # 最多推5步
            if rizhu_tmp['干支'][0:1] in ['甲', '己']:  # 推到甲或己日停止
                break
            if rizhu_tmp['序号'] <= 0:  # 序号0-59
                rizhu_tmp['序号'] += 59
            rizhu_tmp = {'干支': self.Liushijiazilist[rizhu_tmp['序号']-1]['六十甲子'], '序号': rizhu_tmp['序号']-1}  # 按照序号逆推
        if rizhu_tmp['干支'][1:2] in ['子', '午', '卯', '酉']:
            self.Xinxi['三元'] = '上元'
        elif rizhu_tmp['干支'][1:2] in ['寅', '申', '巳', '亥']:
            self.Xinxi['三元'] = '中元'
        elif rizhu_tmp['干支'][1:2] in ['辰', '戌', '丑', '未']:
            self.Xinxi['三元'] = '下元'
        # 遁局：
        dunjubiao = {
            '冬至': [1,7,4],# 阳遁：冬至、惊蛰一七四，小寒二八五，
            '惊蛰': [1,7,4],
            '小寒': [2,8,5],
            '大寒': [3,9,6],# 大寒、春分三九六，雨水九六三，
            '春分': [3,9,6],
            '雨水': [9,6,3],
            '清明': [4,1,7],# 清明、立夏四一七，立春八五二，
            '立夏': [4,1,7],
            '立春': [8,5,2],
            '谷雨': [5,2,8],# 谷雨、小满五二八，芒种六三九。
            '小满': [5,2,8],
            '芒种': [6,3,9],
            '夏至': [9,3,6],# 阴遁：夏至、白露九三六，小暑八二五，
            '白露': [9,3,6],
            '小暑': [8,2,5],
            '大暑': [7,1,4],# 大暑、秋分七一四，立秋二五八，
            '秋分': [7,1,4],
            '立秋': [2,5,8],
            '寒露': [6,9,3],# 寒露、立冬六九三，处暑一四七，
            '立冬': [6,9,3],
            '处暑': [1,4,7],
            '霜降': [5,8,2],# 霜降、小雪五八二，大雪四七一。
            '小雪': [5,8,2],
            '大雪': [4,7,1],
        }
        if self.Xinxi['三元'] == '上元':
            self.Xinxi['遁局'] = dunjubiao[self.Xinxi['节气']][0]
        elif self.Xinxi['三元'] == '中元':
            self.Xinxi['遁局'] = dunjubiao[self.Xinxi['节气']][1]
        elif self.Xinxi['三元'] == '下元':
            self.Xinxi['遁局'] = dunjubiao[self.Xinxi['节气']][2]

    def _dipan(self):
        for i in self.Pan.keys():
            if self.Xinxi['阴阳'] == '阳':
                if self.Pan[i]['宫数'] >= self.Xinxi['遁局']:
                    self.Pan[i]['地干'] = self.sanqiliuyiName[self.Pan[i]['宫数'] - self.Xinxi['遁局']]
                else:
                    self.Pan[i]['地干'] = self.sanqiliuyiName[self.Pan[i]['宫数'] - self.Xinxi['遁局'] + 9]
            else:
                if self.Xinxi['遁局'] >= self.Pan[i]['宫数']:
                    self.Pan[i]['地干'] = self.sanqiliuyiName[self.Xinxi['遁局'] - self.Pan[i]['宫数']]
                else:
                    self.Pan[i]['地干'] = self.sanqiliuyiName[self.Xinxi['遁局'] - self.Pan[i]['宫数'] + 9]

    def _tianpan(self, bujufangfa):
        # 旬首、值符、值使：
        # 1.找出时柱的旬首干，把此干安到地盘时干之上（此是后续排天盘的基准点，如果恰巧是六甲时，则取六仪）。
        # 2.以此干作为地干，以地干所在宫得到宫星、宫门，星为值符，门为值使。
        xun = (int(self.Liushijiazi[self.ganzhi['时柱']]['序号'])-1) // 10
        self.Xinxi['旬首'] = self.Liushijiazilist[xun*10]['六十甲子']
        liuyi = None
        for i in self.Qimentiangan.keys():
            if self.Qimentiangan[i]['六仪旬首'] == self.Xinxi['旬首']:
                liuyi = self.Qimentiangan[i]['天干']
                self.Xinxi['旬首'] += self.Qimentiangan[i]['天干']
        for i in self.Pan.keys():
            self.Pan[i]['天干'] = ''
        xunshougong = None  # 旬首在天盘
        yuanweigong = None  # 时干在地盘
        if self.ganzhi['时柱'][0:1] == '甲':  # 甲时采用六仪干，天干地干相同，成为伏吟局
            for i in self.Pan.keys():
                if self.Pan[i]['地干'] == liuyi:
                    self.Pan[i]['天干'] = liuyi
                    xunshougong = self.Pan[i]
                if self.Pan[i]['地干'] == liuyi:
                    yuanweigong = self.Pan[i]
                    self.Xinxi['值符'] = yuanweigong['宫星']
                    self.Xinxi['值使'] = yuanweigong['宫门']
        else:
            for i in self.Pan.keys():
                if self.Pan[i]['地干'] == self.ganzhi['时柱'][0:1]:
                    self.Pan[i]['天干'] = liuyi
                    xunshougong = self.Pan[i]
                if self.Pan[i]['地干'] == liuyi:
                    yuanweigong = self.Pan[i]
                    self.Xinxi['值符'] = yuanweigong['宫星']
                    self.Xinxi['值使'] = yuanweigong['宫门']
        # 布局方法从这里开始分歧。开始排布天盘
        if bujufangfa == '转盘':
            index = xunshougong['转数']-yuanweigong['转数']  # 旬首干：天干相对地干的位移
            for i in self.Pan.keys():
                for j in self.Pan.keys():
                    if self.Pan[j]['转数'] == (self.Pan[i]['转数'] - index - 8):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                    if self.Pan[j]['转数'] == (self.Pan[i]['转数'] - index):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                    if self.Pan[j]['转数'] == (self.Pan[i]['转数'] - index + 8):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                    if self.Pan[j]['转数'] == (self.Pan[i]['转数'] - index + 16):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                if self.Pan[i]['转数'] == 9:
                    self.Pan[i]['天干'] = '  '
                    self.Pan[i]['天星'] = '  '
        elif bujufangfa == '飞盘':
            index = xunshougong['宫数'] - yuanweigong['宫数']  # 旬首干：天干相对地干的位移
            for i in self.Pan.keys():
                for j in self.Pan.keys():
                    if self.Pan[j]['宫数'] == (self.Pan[i]['宫数'] - index - 9):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                    if self.Pan[j]['宫数'] == (self.Pan[i]['宫数'] - index):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                    if self.Pan[j]['宫数'] == (self.Pan[i]['宫数'] - index + 9):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']
                    if self.Pan[j]['宫数'] == (self.Pan[i]['宫数'] - index + 18):
                        self.Pan[i]['天干'] = self.Pan[j]['地干']
                        self.Pan[i]['天星'] = self.Pan[j]['宫星']

    def _renpan(self):
        pass

    def _shenpan(self):
        pass

    def output(self):
        map_str = ''
        map_str += self.solar['文本'] + '\n'
        map_str += self.solarTerm['文本'] + '\n'
        map_str += self.ganzhi['文本'] + '\n'
        map_str += '起局：' + self.Xinxi['三元'] + '  ' + self.Xinxi['阴阳'] + '遁' + str(self.Xinxi['遁局']) + '局' + '  ' + self.Xinxi['布局方法'] + '法\n'
        map_str += '旬首：' + self.Xinxi['旬首'] + '  值符（星）：' + self.Xinxi['值符'] + '  值使（门）：' + self.Xinxi['值使'] + '\n\n'
        for i in self.Pan.keys():
            # 天盘（上面一行）
            map_str += self.Pan[i]['天干']
            map_str += self.Pan[i]['天星']
            map_str += '' + '|'
            if int(i) % 3 == 0:
                map_str += '\n'
                for j in self.Pan.keys():
                    if (int(j)-1) // 3 == (int(i)-1) // 3:
                        # 地盘（下面一行）
                        map_str += self.Pan[j]['地干']
                        map_str += '  '
                        map_str += '' + '|'
                map_str += '\n'
                map_str += '---- ---- ----'
                map_str += '\n'
        return map_str
