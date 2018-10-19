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

    def paipan(self, lunar, ganzhi, qiguafangfa='标准时间起卦', qiguashuru=None, naganzhifangfa='传统京氏'):
        # 阴阳爻符号
        self.yinyangYao = ['▅▅  ▅▅', '▅▅▅▅▅']
        # 六爻盘格式
        self.Pan = {'10': {'上卦': '  ', '下卦': '  ', '六十四卦': '  ', '卦宫': '', '补充': '  之  '}, '20': {'上卦': '  ', '下卦': '  ', '六十四卦': '  ', '卦宫': '', '补充': ' 日空亡：'},
                    '16': {'六神': '  ', '卦爻': '', '动爻': ' ', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}, '26': {'卦爻': '', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '},
                    '15': {'六神': '  ', '卦爻': '', '动爻': ' ', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}, '25': {'卦爻': '', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '},
                    '14': {'六神': '  ', '卦爻': '', '动爻': ' ', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}, '24': {'卦爻': '', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '},
                    '13': {'六神': '  ', '卦爻': '', '动爻': ' ', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}, '23': {'卦爻': '', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '},
                    '12': {'六神': '  ', '卦爻': '', '动爻': ' ', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}, '22': {'卦爻': '', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '},
                    '11': {'六神': '  ', '卦爻': '', '动爻': ' ', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}, '21': {'卦爻': '', '六亲': '  ', '纳干': ' ', '纳支': ' ', '五行': ' ', '世应': ' '}}
        # 根据不同的起卦方法取不同的卦数
        guashu = None
        dongyao = None
        if qiguafangfa in ['标准时间起卦', '输入动爻时间起卦']:
            guashu, dongyao = self.qigua_shijianqigua(lunar, ganzhi, qiguashuru, qiguafangfa)
        elif qiguafangfa in ['两数字起卦', '三数字起卦', '四数字无动爻起卦', '八数字起卦']:
            guashu, dongyao = self.qigua_shuziqigua(qiguashuru, qiguafangfa)
        elif qiguafangfa == '爻位起卦':
            guashu, dongyao = self.qigua_yaoweiqigua(qiguashuru, qiguafangfa)  # 起卦输入形如：[2,7,5,9,4,1,[1,3,6]]（前6个为爻位数字从上到初，第7个为动爻组）
        # 根据返回的取卦数化卦
        gua, gua_code = self.qigua_huagua(guashu, dongyao)
        # 装卦爻
        self.Pan['16']['卦爻'] = self.yinyangYao[(gua_code[0] & 0b100) >> 2]
        self.Pan['15']['卦爻'] = self.yinyangYao[(gua_code[0] & 0b010) >> 1]
        self.Pan['14']['卦爻'] = self.yinyangYao[(gua_code[0] & 0b001) >> 0]
        self.Pan['13']['卦爻'] = self.yinyangYao[(gua_code[1] & 0b100) >> 2]
        self.Pan['12']['卦爻'] = self.yinyangYao[(gua_code[1] & 0b010) >> 1]
        self.Pan['11']['卦爻'] = self.yinyangYao[(gua_code[1] & 0b001) >> 0]
        self.Pan['26']['卦爻'] = self.yinyangYao[(gua_code[2] & 0b100) >> 2]
        self.Pan['25']['卦爻'] = self.yinyangYao[(gua_code[2] & 0b010) >> 1]
        self.Pan['24']['卦爻'] = self.yinyangYao[(gua_code[2] & 0b001) >> 0]
        self.Pan['23']['卦爻'] = self.yinyangYao[(gua_code[3] & 0b100) >> 2]
        self.Pan['22']['卦爻'] = self.yinyangYao[(gua_code[3] & 0b010) >> 1]
        self.Pan['21']['卦爻'] = self.yinyangYao[(gua_code[3] & 0b001) >> 0]
        self.dongyao = dongyao
        # 装动爻
        for i in self.Pan.keys():
            if self.dongyao:
                for j in self.dongyao:
                    if int(i[1:2]) == j:
                        if self.Pan[i]['卦爻'] == '▅▅  ▅▅':
                            self.Pan[i]['动爻'] = 'X'
                        else:
                            self.Pan[i]['动爻'] = 'O'
        # 装卦名
        self.Pan['10']['上卦'] = gua[0]
        self.Pan['10']['下卦'] = gua[1]
        self.Pan['20']['上卦'] = gua[2]
        self.Pan['20']['下卦'] = gua[3]
        self.Pan['10']['六十四卦'] = gua[4]
        self.Pan['20']['六十四卦'] = gua[5]
        self.Pan['10']['卦宫'] = self.Liushisigua[gua[4]]['卦宫']
        self.Pan['20']['卦宫'] = self.Liushisigua[gua[5]]['卦宫']
        self.Pan['20']['补充'] += ganzhi.split('（')[1].split(' ')[2]
        # 装天干、地支（五行）、世应、六亲、六神
        self.zhuanggua_dizhiwuxing(naganzhifangfa)
        self.zhuanggua_tiangan(ganzhi, naganzhifangfa)
        self.zhuanggua_shiying()
        self.zhuanggua_liuqin()
        self.zhuanggua_liushen(ganzhi)
        return {'农历': lunar, '干支': ganzhi, '八卦': self.Bagua, '动爻': self.dongyao, '盘': self.Pan}

    def output(self):
        map_str = ''
        for i in self.Pan.keys():
            if i == '10' or i == '20':
                map_str += '上'
                map_str += self.Pan[i]['上卦']
                map_str += '下'
                map_str += self.Pan[i]['下卦']
                map_str += ' '
                map_str += self.Pan[i]['六十四卦']
                map_str += '('
                map_str += self.Pan[i]['卦宫']
                map_str += '宫)'
                map_str += self.Pan[i]['补充']
                if i[0:1] == '2':
                    map_str += '\n'
            else:
                if i[0:1] == '1':
                    map_str += self.Pan[i]['六神']
                map_str += self.Pan[i]['卦爻']
                if i[0:1] == '1':
                    map_str += self.Pan[i]['动爻']
                map_str += self.Pan[i]['六亲']
                map_str += self.Pan[i]['纳干']
                map_str += self.Pan[i]['纳支']
                map_str += self.Pan[i]['五行']
                map_str += self.Pan[i]['世应']
                if i[0:1] == '1':
                    map_str += '\t'
                if i[0:1] == '2':
                    map_str += '\n'
        print(map_str)

    def qigua_shijianqigua(self, lunar, ganzhi, qiguashuru, qiguafangfa):
        # 时间起卦法
        bengua_shang_num = None
        bengua_xia_num = None
        dongyao = []
        if qiguafangfa == '标准时间起卦':
            # 此时的起卦输入作为灵动数，灵动数加入到本卦下卦数，影响本卦下卦
            # 纳甲筮法时间取数法（本卦：（年+月+日）%8，（年+月+日+时）%8，动爻：（年+月+日+时）%6，取先天八卦数）。余0取坤
            # 求年月日时数
            nianshu = self.dizhiName.index(ganzhi.split('：')[1].split(' ')[0][1:2]) + 1
            yueshu = lunar[2]
            rishu = lunar[3]
            shishu = lunar[4]
            # 根据时间计算取卦数
            bengua_shang_num = (nianshu + yueshu + rishu) % 8
            if bengua_shang_num == 0:
                bengua_shang_num += 8
            # 判断是否加入灵动数，影响下卦和动爻
            if qiguashuru is None:
                bengua_xia_num = (nianshu + yueshu + rishu + shishu) % 8
                dongyao.append((nianshu + yueshu + rishu + shishu) % 6)
            else:
                bengua_xia_num = (nianshu + yueshu + rishu + shishu + qiguashuru[0]) % 8
                dongyao.append((nianshu + yueshu + rishu + shishu + qiguashuru[0]) % 6)
            if bengua_xia_num == 0:
                bengua_xia_num += 8
            if dongyao[0] == 0:
                dongyao[0] += 6
        # 此时的起卦输入作为动爻(1-6)，可多动，影响变卦
        elif qiguafangfa == '输入动爻时间起卦':
            # 求年月日时数
            nianshu = self.dizhiName.index(ganzhi.split('：')[1].split(' ')[0][1:2]) + 1
            yueshu = lunar[2]
            rishu = lunar[3]
            shishu = lunar[4]
            # 根据时间计算取卦数
            bengua_shang_num = (nianshu + yueshu + rishu) % 8
            if bengua_shang_num == 0:
                bengua_shang_num += 8
            bengua_xia_num = (nianshu + yueshu + rishu + shishu) % 8
            if bengua_xia_num == 0:
                bengua_xia_num += 8
            # 根据起卦输入确定动爻
            for i in qiguashuru:
                if i not in dongyao:
                    dongyao.append(i)
        return [bengua_shang_num, bengua_xia_num], dongyao

    def qigua_shuziqigua(self, qiguashuru, qiguafangfa):
        # 数字起卦法
        # 同样采用先天八卦纳数
        guashu = []
        dongyao = []
        if qiguafangfa == '两数字起卦':
            bengua_shang_num = qiguashuru[0] % 8
            if bengua_shang_num == 0:
                bengua_shang_num += 8
            bengua_xia_num = qiguashuru[1] % 8
            if bengua_xia_num == 0:
                bengua_xia_num += 8
            dongyao.append((qiguashuru[0] + qiguashuru[1]) % 6)
            if dongyao[0] == 0:
                dongyao[0] += 6
            guashu.append(bengua_shang_num)
            guashu.append(bengua_xia_num)
        elif qiguafangfa == '三数字起卦':
            bengua_shang_num = qiguashuru[0] % 8
            if bengua_shang_num == 0:
                bengua_shang_num += 8
            bengua_xia_num = qiguashuru[1] % 8
            if bengua_xia_num == 0:
                bengua_xia_num += 8
            dongyao.append((qiguashuru[0] + qiguashuru[1] + qiguashuru[2]) % 6)
            if dongyao[0] == 0:
                dongyao[0] += 6
            guashu.append(bengua_shang_num)
            guashu.append(bengua_xia_num)
        elif qiguafangfa == '四数字无动爻起卦':
            bengua_shang_num = qiguashuru[0] % 8
            if bengua_shang_num == 0:
                bengua_shang_num += 8
            bengua_xia_num = qiguashuru[1] % 8
            if bengua_xia_num == 0:
                bengua_xia_num += 8
            biangua_shang_num = qiguashuru[2] % 8
            if biangua_shang_num == 0:
                biangua_shang_num += 8
            biangua_xia_num = qiguashuru[3] % 8
            if biangua_xia_num == 0:
                biangua_xia_num += 8
            guashu.append(bengua_shang_num)
            guashu.append(bengua_xia_num)
            guashu.append(biangua_shang_num)
            guashu.append(biangua_xia_num)
        elif qiguafangfa == '八数字起卦':
            pass
        return guashu, dongyao

    def qigua_yaoweiqigua(self, qiguashuru, qiguafangfa):
        # 爻位起卦法
        bengua_shang_num = None
        bengua_xia_num = None
        dongyao = []
        # 此时的起卦输入前6个为爻位数字，第7个为动爻数组
        yaowei_code = []
        for i in range(0, 6):
            if qiguashuru[i] in [1, 3, 5, 7, 9]:
                yaowei_code.append(1)  # 奇数为阳1
            else:
                yaowei_code.append(0)
        bengua_shang_code = yaowei_code[0]*4 + yaowei_code[1]*2 + yaowei_code[2]*1
        bengua_xia_code = yaowei_code[3] * 4 + yaowei_code[4] * 2 + yaowei_code[5] * 1
        for i in self.Bagua.keys():
            if eval(self.Bagua[i]['二进制']) == bengua_shang_code:
                bengua_shang_num = self.Bagua[i]['先天卦数']
            if eval(self.Bagua[i]['二进制']) == bengua_xia_code:
                bengua_xia_num = self.Bagua[i]['先天卦数']
        for i in qiguashuru[6]:
            if i not in dongyao:
                dongyao.append(i)
        return [bengua_shang_num, bengua_xia_num], dongyao

    def qigua_huagua(self, guashu, dongyao):
        # 根据取卦数取卦，按照先天八卦数取卦
        bengua_shang_num = guashu[0]
        bengua_xia_num = guashu[1]
        bengua_xia = None
        bengua_shang = None
        biangua_xia = None
        biangua_shang = None
        bengua_shang_code = None
        bengua_xia_code = None
        biangua_shang_code = None
        biangua_xia_code = None
        for i in self.Bagua.keys():
            if bengua_shang_num == self.Bagua[i]['先天卦数']:
                bengua_shang = i
                bengua_shang_code = eval(self.Bagua[i]['二进制'])
            if bengua_xia_num == self.Bagua[i]['先天卦数']:
                bengua_xia = i
                bengua_xia_code = eval(self.Bagua[i]['二进制'])
        # 求本卦的六十四卦
        bengua = None
        bengua_code = None
        for i in self.Liushisigua.keys():
            if self.Liushisigua[i]['上卦名'] == bengua_shang and self.Liushisigua[i]['下卦名'] == bengua_xia:
                bengua = i
                bengua_code = eval(self.Liushisigua[i]['二进制'])
        # 动爻可有0个（用单个0表示）、1个或多个
        # 无动爻则卦数必然有4个，变卦根据后两个卦数得来
        if len(dongyao) == 0:
            biangua_shang_num = guashu[2]
            biangua_xia_num = guashu[3]
            for i in self.Bagua.keys():
                if biangua_shang_num == self.Bagua[i]['先天卦数']:
                    biangua_shang = i
                    biangua_shang_code = eval(self.Bagua[i]['二进制'])
                if biangua_xia_num == self.Bagua[i]['先天卦数']:
                    biangua_xia = i
                    biangua_xia_code = eval(self.Bagua[i]['二进制'])
        # 有动爻，则卦数只有两个，变卦由本卦和动爻计算得来
        elif len(dongyao) >= 1:
            dongyao_code = 0
            for i in dongyao:
                dongyao_code += 2 ** (i - 1)
            biangua_code = eval(self.Liushisigua[bengua]['二进制']) ^ dongyao_code
            biangua_shang_code = biangua_code // 8  # 取前三位
            biangua_xia_code = biangua_code % 8  # 取后三位
            for i in self.Bagua.keys():
                if biangua_shang_code == eval(self.Bagua[i]['二进制']):
                    biangua_shang = i
                if biangua_xia_code == eval(self.Bagua[i]['二进制']):
                    biangua_xia = i
        # 求变卦的六十四卦
        biangua = None
        biangua_code = None
        for i in self.Liushisigua.keys():
            if self.Liushisigua[i]['上卦名'] == biangua_shang and self.Liushisigua[i]['下卦名'] == biangua_xia:
                biangua = i
                biangua_code = eval(self.Liushisigua[i]['二进制'])
        return [bengua_shang, bengua_xia, biangua_shang, biangua_xia, bengua, biangua], [bengua_shang_code, bengua_xia_code, biangua_shang_code, biangua_xia_code, bengua_code, biangua_code]

    def zhuanggua_dizhiwuxing(self, naganzhifangfa):
        if naganzhifangfa == '传统京氏':
            # 乾卦从最下面起的三爻为子，寅，辰；上面三爻为午，申，戌；
            # 兑卦从最下面起的三爻为巳，卯，丑；上面三爻为亥，酉，未；
            # 离卦从最下面起的三爻为卯，丑，亥；上面三爻为酉，未，巳；
            # 震卦从最下面起的三爻为子，寅，辰；上面三爻为午，申，戌；
            # 巽卦从最下面起的三爻为丑，亥，酉；上面三爻为未，巳，卯；
            # 坎卦从最下面起的三爻为寅，辰，午；上面三爻为申，戌，子；
            # 艮卦从最下面起的三爻为辰，午，申；上面三爻为戌，子，寅；
            # 坤卦从最下面起的三爻为未，巳，卯；上面三爻为丑，亥，酉；
            nazhi = {'乾': ['子', '寅', '辰', '午', '申', '戌'],
                     '兑': ['巳', '卯', '丑', '亥', '酉', '未'],
                     '离': ['卯', '丑', '亥', '酉', '未', '巳'],
                     '震': ['子', '寅', '辰', '午', '申', '戌'],
                     '巽': ['丑', '亥', '酉', '未', '巳', '卯'],
                     '坎': ['寅', '辰', '午', '申', '戌', '子'],
                     '艮': ['辰', '午', '申', '戌', '子', '寅'],
                     '坤': ['未', '巳', '卯', '丑', '亥', '酉']}
        elif naganzhifangfa == '先天甲子易':
            # 乾卦从最下面起的三爻为子，寅，辰；上面三爻为午，申，戌；
            # 兑卦从最下面起的三爻为巳，卯，丑；上面三爻为亥，酉，未；
            # 离卦从最下面起的三爻为卯，丑，亥；上面三爻为酉，未，巳；
            # 震卦从最下面起的三爻为午，申，戌；上面三爻为子，寅，辰；
            # 巽卦从最下面起的三爻为丑，亥，酉；上面三爻为未，巳，卯；
            # 坎卦从最下面起的三爻为辰，午，申；上面三爻为戌，子，寅；
            # 艮卦从最下面起的三爻为寅，辰，午；上面三爻为申，戌，子；
            # 坤卦从最下面起的三爻为未，巳，卯；上面三爻为丑，亥，酉；
            nazhi = {'乾': ['子', '寅', '辰', '午', '申', '戌'],
                     '兑': ['巳', '卯', '丑', '亥', '酉', '未'],
                     '离': ['卯', '丑', '亥', '酉', '未', '巳'],
                     '震': ['午', '申', '戌', '子', '寅', '辰'],
                     '巽': ['丑', '亥', '酉', '未', '巳', '卯'],
                     '坎': ['辰', '午', '申', '戌', '子', '寅'],
                     '艮': ['寅', '辰', '午', '申', '戌', '子'],
                     '坤': ['未', '巳', '卯', '丑', '亥', '酉']}
        bengua_xiagua = self.Pan['10']['下卦']
        biangua_xiagua = self.Pan['20']['下卦']
        bengua_shanggua = self.Pan['10']['上卦']
        biangua_shanggua = self.Pan['20']['上卦']
        for i in range(0, 6):
            if i < 3:
                self.Pan['1' + str(i + 1)]['纳支'] = nazhi[bengua_xiagua][i]
                self.Pan['1' + str(i + 1)]['五行'] = self.Dizhi[self.Pan['1' + str(i + 1)]['纳支']]['五行']
                self.Pan['2' + str(i + 1)]['纳支'] = nazhi[biangua_xiagua][i]
                self.Pan['2' + str(i + 1)]['五行'] = self.Dizhi[self.Pan['2' + str(i + 1)]['纳支']]['五行']
            else:
                self.Pan['1' + str(i + 1)]['纳支'] = nazhi[bengua_shanggua][i]
                self.Pan['1' + str(i + 1)]['五行'] = self.Dizhi[self.Pan['1' + str(i + 1)]['纳支']]['五行']
                self.Pan['2' + str(i + 1)]['纳支'] = nazhi[biangua_shanggua][i]
                self.Pan['2' + str(i + 1)]['五行'] = self.Dizhi[self.Pan['2' + str(i + 1)]['纳支']]['五行']

    def zhuanggua_tiangan(self, ganzhi, naganzhifangfa):
        if naganzhifangfa == '传统京氏':
            # 乾纳甲壬坎纳戊
            # 离纳己土震纳庚
            # 坤纳乙癸巽纳辛
            # 艮纳丙火兑纳丁
            nagan = {'乾': ['甲', '壬'],
                     '兑': ['丁', '丁'],
                     '离': ['己', '己'],
                     '震': ['庚', '庚'],
                     '巽': ['辛', '辛'],
                     '坎': ['戊', '戊'],
                     '艮': ['丙', '丙'],
                     '坤': ['乙', '癸']}
            for i in self.Pan.keys():
                if i[1:2] in ['1', '2', '3']:  # 下卦
                    self.Pan[i]['纳干'] = nagan[self.Pan[i[0:1] + '0']['下卦']][0]
                if i[1:2] in ['4', '5', '6']:  # 上卦
                    self.Pan[i]['纳干'] = nagan[self.Pan[i[0:1] + '0']['上卦']][1]
        elif naganzhifangfa == '先天甲子易':
            rigan = ganzhi.split('：')[1].split(' ')[2][0:1]
            # 五子元遁
            if rigan in ['甲', '己']:
                gan_index = 1  # 甲子
            elif rigan in ['乙', '庚']:
                gan_index = 3  # 丙子
            elif rigan in ['丙', '辛']:
                gan_index = 5  # 戊子
            elif rigan in ['丁', '壬']:
                gan_index = 7  # 庚子
            elif rigan in ['戊', '癸']:
                gan_index = 9  # 壬子
            else:
                gan_index = 1
            for i in self.Pan.keys():
                if i == '10' or i == '20':
                    continue
                idx = self.dizhiName.index(self.Pan[i]['纳支']) + gan_index - 1
                if idx >= 10:
                    idx -= 10
                self.Pan[i]['纳干'] = self.tianganName[idx]

    def zhuanggua_shiying(self):
        # 天同二世天变五
        # 地同四世地变初
        # 人同游魂（四世）人变归（三世）
        # 本宫六世三世异
        for i in range(0, 2):
            # 天同二世
            if self.Pan[str(i + 1) + '3']['卦爻'] == self.Pan[str(i + 1) + '6']['卦爻'] \
                    and self.Pan[str(i + 1) + '1']['卦爻'] != self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '2']['卦爻'] != self.Pan[str(i + 1) + '5']['卦爻']:
                self.Pan[str(i + 1) + '2']['世应'] = '世'
                self.Pan[str(i + 1) + '5']['世应'] = '应'
            # 天变五
            if self.Pan[str(i + 1) + '3']['卦爻'] != self.Pan[str(i + 1) + '6']['卦爻'] \
                    and self.Pan[str(i + 1) + '1']['卦爻'] == self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '2']['卦爻'] == self.Pan[str(i + 1) + '5']['卦爻']:
                self.Pan[str(i + 1) + '5']['世应'] = '世'
                self.Pan[str(i + 1) + '2']['世应'] = '应'
            # 地同四世
            if self.Pan[str(i + 1) + '1']['卦爻'] == self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '2']['卦爻'] != self.Pan[str(i + 1) + '5']['卦爻'] \
                    and self.Pan[str(i + 1) + '3']['卦爻'] != self.Pan[str(i + 1) + '6']['卦爻']:
                self.Pan[str(i + 1) + '4']['世应'] = '世'
                self.Pan[str(i + 1) + '1']['世应'] = '应'
            # 地变初
            if self.Pan[str(i + 1) + '1']['卦爻'] != self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '2']['卦爻'] == self.Pan[str(i + 1) + '5']['卦爻'] \
                    and self.Pan[str(i + 1) + '3']['卦爻'] == self.Pan[str(i + 1) + '6']['卦爻']:
                self.Pan[str(i + 1) + '1']['世应'] = '世'
                self.Pan[str(i + 1) + '4']['世应'] = '应'
            # 人同游魂（四世）
            if self.Pan[str(i + 1) + '2']['卦爻'] == self.Pan[str(i + 1) + '5']['卦爻'] \
                    and self.Pan[str(i + 1) + '1']['卦爻'] != self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '3']['卦爻'] != self.Pan[str(i + 1) + '6']['卦爻']:
                self.Pan[str(i + 1) + '4']['世应'] = '世'
                self.Pan[str(i + 1) + '1']['世应'] = '应'
            # 人变归（三世）
            if self.Pan[str(i + 1) + '2']['卦爻'] != self.Pan[str(i + 1) + '5']['卦爻'] \
                    and self.Pan[str(i + 1) + '1']['卦爻'] == self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '3']['卦爻'] == self.Pan[str(i + 1) + '6']['卦爻']:
                self.Pan[str(i + 1) + '3']['世应'] = '世'
                self.Pan[str(i + 1) + '6']['世应'] = '应'
            # 本宫六世
            if self.Pan[str(i + 1) + '3']['卦爻'] == self.Pan[str(i + 1) + '6']['卦爻'] \
                    and self.Pan[str(i + 1) + '1']['卦爻'] == self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '2']['卦爻'] == self.Pan[str(i + 1) + '5']['卦爻']:
                self.Pan[str(i + 1) + '6']['世应'] = '世'
                self.Pan[str(i + 1) + '3']['世应'] = '应'
            # 三世异
            if self.Pan[str(i + 1) + '3']['卦爻'] != self.Pan[str(i + 1) + '6']['卦爻'] \
                    and self.Pan[str(i + 1) + '1']['卦爻'] != self.Pan[str(i + 1) + '4']['卦爻'] \
                    and self.Pan[str(i + 1) + '2']['卦爻'] != self.Pan[str(i + 1) + '5']['卦爻']:
                self.Pan[str(i + 1) + '3']['世应'] = '世'
                self.Pan[str(i + 1) + '6']['世应'] = '应'

    def zhuanggua_liuqin(self):
        # 首先确定得出的本卦是何宫（八宫六十四卦）
        # 然后以这个五行为“我”，根据所纳地支的五行，依“生我者父母，我生者子孙，克我者官鬼，我克者妻财，相同者兄弟”的关系来定六亲
        bengua_wuxing = self.Bagua[self.Pan['10']['卦宫']]['五行']
        fumu = self.db2cdata.get_wuxing_shengke(bengua_wuxing, return_type='生')
        zisun = self.db2cdata.get_wuxing_shengke(bengua_wuxing, return_type='泄')
        guangui = self.db2cdata.get_wuxing_shengke(bengua_wuxing, return_type='克')
        qicai = self.db2cdata.get_wuxing_shengke(bengua_wuxing, return_type='耗')
        xiongdi = self.db2cdata.get_wuxing_shengke(bengua_wuxing, return_type='助')
        for i in range(0, 6):
            if self.Pan['1' + str(i + 1)]['五行'] == fumu:
                self.Pan['1' + str(i + 1)]['六亲'] = '父母'
            if self.Pan['1' + str(i + 1)]['五行'] == zisun:
                self.Pan['1' + str(i + 1)]['六亲'] = '子孙'
            if self.Pan['1' + str(i + 1)]['五行'] == guangui:
                self.Pan['1' + str(i + 1)]['六亲'] = '官鬼'
            if self.Pan['1' + str(i + 1)]['五行'] == qicai:
                self.Pan['1' + str(i + 1)]['六亲'] = '妻财'
            if self.Pan['1' + str(i + 1)]['五行'] == xiongdi:
                self.Pan['1' + str(i + 1)]['六亲'] = '兄弟'
            if self.Pan['2' + str(i + 1)]['五行'] == fumu:
                self.Pan['2' + str(i + 1)]['六亲'] = '父母'
            if self.Pan['2' + str(i + 1)]['五行'] == zisun:
                self.Pan['2' + str(i + 1)]['六亲'] = '子孙'
            if self.Pan['2' + str(i + 1)]['五行'] == guangui:
                self.Pan['2' + str(i + 1)]['六亲'] = '官鬼'
            if self.Pan['2' + str(i + 1)]['五行'] == qicai:
                self.Pan['2' + str(i + 1)]['六亲'] = '妻财'
            if self.Pan['2' + str(i + 1)]['五行'] == xiongdi:
                self.Pan['2' + str(i + 1)]['六亲'] = '兄弟'

    def zhuanggua_liushen(self, ganzhi):
        # 根据日干：甲乙起青龙，丙丁起朱雀，戊日起勾陈，己日起腾蛇，庚辛起白虎，壬癸起玄武（正好是对应的五行）
        # 按照青龙、朱雀、勾陈、腾蛇、白虎、玄武的顺序，由初爻装至六爻
        rigan = ganzhi.split('：')[1].split(' ')[2][0:1]
        liushen = ['青龙', '朱雀', '勾陈', '腾蛇', '白虎', '玄武']
        idx = 0
        if rigan in ['甲', '乙']:
            idx = 0
        if rigan in ['丙', '丁']:
            idx = 1
        if rigan in ['戊']:
            idx = 2
        if rigan in ['己']:
            idx = 3
        if rigan in ['庚', '辛']:
            idx = 4
        if rigan in ['壬', '癸']:
            idx = 5
        for i in range(0, 6):
            if i + idx > 5:
                idx -= 6
            self.Pan['1' + str(i + 1)]['六神'] = liushen[i + idx]
            self.Pan['2' + str(i + 1)]['六神'] = liushen[i + idx]
