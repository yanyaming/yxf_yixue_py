#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.db import Db
from utils.db2cdata import Db2Cdata


class Paipan:
    def __init__(self):
        # 地支表
        self.dizhiName = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')
        # 洛书九宫表
        self.Pan = {'1': {'宫数': 4, '宫卦': '巽'}, '2': {'宫数': 9, '宫卦': '离'}, '3': {'宫数': 2, '宫卦': '坤'},
                    '4': {'宫数': 3, '宫卦': '震'}, '5': {'宫数': 5, '宫卦': '中'}, '6': {'宫数': 7, '宫卦': '兑'},
                    '7': {'宫数': 8, '宫卦': '艮'}, '8': {'宫数': 1, '宫卦': '坎'}, '9': {'宫数': 6, '宫卦': '乾'}}
        # 导入卦数据
        self.db = Db()
        self.db2cdata = Db2Cdata()
        self.Wuxing = self.db.get_tabledict_dict("[基础表-五行]")
        self.Tiangan = self.db.get_tabledict_dict("[基础表-十天干]")
        self.Dizhi = self.db.get_tabledict_dict("[基础表-十二地支]")
        self.Bagua = self.db.get_tabledict_dict("[基础表-八卦]")
        self.Liushisigua = self.db.get_tabledict_dict("[基础表-六十四卦]")
        self.Liushijiazi = self.db.get_tabledict_dict("[基础表-六十甲子]")
        self.Luoshu = self.db.get_tabledict_dict("[基础表-洛书九宫格]")

    def paipan(self, lunar, ganzhi, lingdongshu=None, shuziqigua=None, guizangfangfa='四正'):
        # 起卦
        if shuziqigua is None:
            gua, gua_code = self.qigua_shijianqigua(lunar, ganzhi, lingdongshu)
        elif len(shuziqigua) == 8 or len(shuziqigua) == 4:
            gua, gua_code = self.qigua_shuziqigua(shuziqigua)
        else:
            return '', '', ''
        # 根据本卦和变卦进行各种组合，排盘
        # 把本卦、变卦共4个填入上下左右4个宫
        self.Pan['2']['单卦'] = gua[0]  # 本卦上
        self.Pan['8']['单卦'] = gua[1]  # 本卦下
        self.Pan['4']['单卦'] = gua[2]  # 变卦上
        self.Pan['6']['单卦'] = gua[3]  # 变卦下
        self.Pan['2']['重卦'] = gua[4]
        self.Pan['8']['重卦'] = gua[4]
        self.Pan['4']['重卦'] = gua[5]
        self.Pan['6']['重卦'] = gua[5]
        # 求互卦
        hugua, hugua_code = self.qigua_hugua(gua_code, shuziqigua)
        self.Pan['1']['单卦'] = hugua[0]
        self.Pan['3']['单卦'] = hugua[1]
        self.Pan['7']['单卦'] = hugua[2]
        self.Pan['9']['单卦'] = hugua[3]
        self.Pan['1']['重卦'] = hugua[4]
        self.Pan['3']['重卦'] = hugua[4]
        self.Pan['7']['重卦'] = hugua[5]
        self.Pan['9']['重卦'] = hugua[5]
        # 归藏法求中宫卦
        guizang, guizang_code = self.qigua_guizang(guizangfangfa, gua_code, hugua_code)
        self.Pan['5']['单卦'] = guizang[0]
        if guizang[2] is not None:
            self.Pan['5']['重卦'] = guizang[2]
        else:
            self.Pan['5']['重卦'] = ''
        # 卦气升降↑↓
        bengua_shengjiang = self.Bagua[self.Pan['2']['单卦']]['升降'] + self.Bagua[self.Pan['8']['单卦']]['升降']
        biangua_shengjiang = self.Bagua[self.Pan['4']['单卦']]['升降'] + self.Bagua[self.Pan['6']['单卦']]['升降']
        bengua_hugua_shengjiang = self.Bagua[self.Pan['1']['单卦']]['升降'] + self.Bagua[self.Pan['3']['单卦']]['升降']
        biangua_hugua_shengjiang = self.Bagua[self.Pan['7']['单卦']]['升降'] + self.Bagua[self.Pan['9']['单卦']]['升降']
        if guizang[1] is not None:
            zhonggong_shengjiang = self.Bagua[guizang[0]]['升降'] + self.Bagua[guizang[1]]['升降']
        else:
            zhonggong_shengjiang = ''
        self.Pan['2']['升降'] = bengua_shengjiang
        self.Pan['8']['升降'] = bengua_shengjiang
        self.Pan['4']['升降'] = biangua_shengjiang
        self.Pan['6']['升降'] = biangua_shengjiang
        self.Pan['1']['升降'] = bengua_hugua_shengjiang
        self.Pan['3']['升降'] = bengua_hugua_shengjiang
        self.Pan['7']['升降'] = biangua_hugua_shengjiang
        self.Pan['9']['升降'] = biangua_hugua_shengjiang
        self.Pan['5']['升降'] = zhonggong_shengjiang
        # 卦气阴阳
        for i in self.Pan.keys():
            self.Pan[i]['阴阳'] = self.Bagua[self.Pan[i]['单卦']]['阴阳']
        # 卦之大中小
        for i in self.Pan.keys():
            self.Pan[i]['三分'] = self.Bagua[self.Pan[i]['单卦']]['三分']
        return {'农历': lunar, '干支': ganzhi, '八卦': self.Bagua, '六十四卦': self.Liushisigua, '动爻': self.dongyao, '盘': self.Pan}

    def output(self):
        map_str = ''
        for i in self.Pan.keys():
            map_str += str(self.Pan[i]['宫数'])
            map_str += self.Pan[i]['单卦']
            map_str += self.Pan[i]['重卦']
            if self.Pan[i]['升降'][0:1] == '升':
                map_str += '↑'
            if self.Pan[i]['升降'][0:1] == '降':
                map_str += '↓'
            if self.Pan[i]['升降'][1:2] == '升':
                map_str += '↑'
            if self.Pan[i]['升降'][1:2] == '降':
                map_str += '↓'
            map_str += self.Pan[i]['阴阳']
            map_str += self.Pan[i]['三分']
            map_str += '' + '|'
            if int(i) % 3 == 0:
                map_str += '\n'
                map_str += '------\t------\t------\t------\t------\t------'
                map_str += '\n'
        print(map_str)

    def qigua_shijianqigua(self, lunar, ganzhi, lingdongshu):
        # 时间起卦法
        # 梅花易数时间取数法（本卦：（年+月+日）%8，（年+月+日+时）%8，动爻：（年+月+日）%6，取先天八卦数）。余0取坤
        # 有缺陷：变卦只有一个动爻，上下卦只有一个变化
        # 求年月日时数
        nianshu = self.dizhiName.index(ganzhi.split('：')[1].split(' ')[0][1:2]) + 1
        yueshu = lunar[0][2]
        rishu = lunar[0][3]
        shishu = lunar[0][4]
        # 根据时间计算取卦数
        bengua_shang_num = (nianshu + yueshu + rishu) % 8
        if bengua_shang_num == 0:
            bengua_shang_num += 8
        bengua_xia_num = (nianshu + yueshu + rishu + shishu) % 8
        if bengua_xia_num == 0:
            bengua_xia_num += 8
        dongyao = (nianshu + yueshu + rishu + shishu) % 6
        if dongyao == 0:
            dongyao += 6
        self.dongyao = dongyao
        # 根据取卦数取卦
        bengua_xia = None
        bengua_shang = None
        biangua_xia = None
        biangua_shang = None
        bengua_shang_code = None
        bengua_xia_code = None
        biangua_shang_code = None
        biangua_xia_code = None
        for i in self.Bagua.keys():
            if bengua_shang_num == int(self.Bagua[i]['先天卦数']):
                bengua_shang = i
                bengua_shang_code = eval(self.Bagua[i]['二进制'])
            if bengua_xia_num == int(self.Bagua[i]['先天卦数']):
                bengua_xia = i
                bengua_xia_code = eval(self.Bagua[i]['二进制'])
        if 1 <= dongyao <= 3:
            dongyao_code = 2 ** (dongyao - 1)
            biangua_xia_code = eval(self.Bagua[bengua_xia]['二进制']) ^ dongyao_code  # 按位异或，即可对特定位取反，实现动爻阴阳相反的效果
            biangua_shang_code = eval(self.Bagua[bengua_shang]['二进制'])  # 万能语句eval()，执行字符串内的一切表达，把'0b001'字符串执行成为二进制数字
        if 4 <= dongyao <= 6:
            dongyao_code = 2 ** (dongyao - 4)
            biangua_shang_code = eval(self.Bagua[bengua_shang]['二进制']) ^ dongyao_code
            biangua_xia_code = eval(self.Bagua[bengua_xia]['二进制'])
        for i in self.Bagua.keys():
            if biangua_shang_code == eval(self.Bagua[i]['二进制']):
                biangua_shang = i
            if biangua_xia_code == eval(self.Bagua[i]['二进制']):
                biangua_xia = i
        # 求六十四卦
        bengua = None
        bengua_code = None
        biangua = None
        biangua_code = None
        for i in self.Liushisigua.keys():
            if self.Liushisigua[i]['上卦名'] == bengua_shang and self.Liushisigua[i]['下卦名'] == bengua_xia:
                bengua = i
                bengua_code = eval(self.Liushisigua[i]['二进制'])
            if self.Liushisigua[i]['上卦名'] == biangua_shang and self.Liushisigua[i]['下卦名'] == biangua_xia:
                biangua = i
                biangua_code = eval(self.Liushisigua[i]['二进制'])
        return [bengua_shang, bengua_xia, biangua_shang, biangua_xia, bengua, biangua], [bengua_shang_code, bengua_xia_code, biangua_shang_code, biangua_xia_code, bengua_code, biangua_code]

    def qigua_shuziqigua(self, shuziqigua):
        # 数字起卦法
        # 同样采用先天八卦纳数
        bengua_shang_num = shuziqigua[0] % 8
        if bengua_shang_num == 0:
            bengua_shang_num += 8
        bengua_xia_num = shuziqigua[1] % 8
        if bengua_xia_num == 0:
            bengua_xia_num += 8
        biangua_shang_num = shuziqigua[2] % 8
        if biangua_shang_num == 0:
            biangua_shang_num += 8
        biangua_xia_num = shuziqigua[3] % 8
        if biangua_xia_num == 0:
            biangua_xia_num += 8
        self.dongyao = 0  # 数字起卦不需要动爻
        # 根据取卦数取卦
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
            if biangua_shang_num == self.Bagua[i]['先天卦数']:
                biangua_shang = i
                biangua_shang_code = eval(self.Bagua[i]['二进制'])
            if biangua_xia_num == self.Bagua[i]['先天卦数']:
                biangua_xia = i
                biangua_xia_code = eval(self.Bagua[i]['二进制'])
        # 求六十四卦
        bengua = None
        bengua_code = None
        biangua = None
        biangua_code = None
        for i in self.Liushisigua.keys():
            if self.Liushisigua[i]['上卦名'] == bengua_shang and self.Liushisigua[i]['下卦名'] == bengua_xia:
                bengua = i
                bengua_code = eval(self.Liushisigua[i]['二进制'])
            if self.Liushisigua[i]['上卦名'] == biangua_shang and self.Liushisigua[i]['下卦名'] == biangua_xia:
                biangua = i
                biangua_code = eval(self.Liushisigua[i]['二进制'])
        return [bengua_shang, bengua_xia, biangua_shang, biangua_xia, bengua, biangua], [bengua_shang_code, bengua_xia_code, biangua_shang_code, biangua_xia_code, bengua_code, biangua_code]

    def qigua_hugua(self, gua_code, shuziqigua):
        # 互卦
        if shuziqigua is None:
            hugua = []
            hugua_code = []
            chonggua = [0, 0]
            chonggua[0] += gua_code[0]*8 + gua_code[1]
            chonggua[1] += gua_code[2]*8 + gua_code[3]
            # 互卦求法：从下到上（低位到高位）依次是原卦的2、3、4、3、4、5爻
            # 例：011110 011101
            code1 = ((chonggua[0]&0b000010)>>1)+((chonggua[0]&0b000100)>>1)+((chonggua[0]&0b001000)>>1)+\
                    ((chonggua[0]&0b000100)<<1)+((chonggua[0]&0b001000)<<1)+((chonggua[0]&0b010000)<<1)  # 111111
            code2 = ((chonggua[1]&0b000010)>>1)+((chonggua[1]&0b000100)>>1)+((chonggua[1]&0b001000)>>1)+\
                    ((chonggua[1]&0b000100)<<1)+((chonggua[1]&0b001000)<<1)+((chonggua[1]&0b010000)<<1)  # 111110
            hugua_code.append(code1//8)
            hugua_code.append(code1 % 8)
            hugua_code.append(code2//8)
            hugua_code.append(code2 % 8)
            bengua_shang_hugua, bengua_xia_hugua, biangua_shang_hugua, biangua_xia_hugua = None, None, None, None
            for i in self.Bagua.keys():
                if hugua_code[0] == eval(self.Bagua[i]['二进制']):
                    bengua_shang_hugua = i
                if hugua_code[1] == eval(self.Bagua[i]['二进制']):
                    bengua_xia_hugua = i
                if hugua_code[2] == eval(self.Bagua[i]['二进制']):
                    biangua_shang_hugua = i
                if hugua_code[3] == eval(self.Bagua[i]['二进制']):
                    biangua_xia_hugua = i
            hugua.append(bengua_shang_hugua)
            hugua.append(bengua_xia_hugua)
            hugua.append(biangua_shang_hugua)
            hugua.append(biangua_xia_hugua)
        else:
            hugua = []
            hugua_code = []
            bengua_hugua_shang_num = shuziqigua[4] % 8
            if bengua_hugua_shang_num == 0:
                bengua_hugua_shang_num += 8
            bengua_hugua_xia_num = shuziqigua[5] % 8
            if bengua_hugua_xia_num == 0:
                bengua_hugua_xia_num += 8
            biangua_hugua_shang_num = shuziqigua[6] % 8
            if biangua_hugua_shang_num == 0:
                biangua_hugua_shang_num += 8
            biangua_hugua_xia_num = shuziqigua[7] % 8
            if biangua_hugua_xia_num == 0:
                biangua_hugua_xia_num += 8
            bengua_shang_hugua_code, bengua_xia_hugua_code, biangua_shang_hugua_code, biangua_xia_hugua_code = None, None, None, None
            bengua_shang_hugua, bengua_xia_hugua, biangua_shang_hugua, biangua_xia_hugua = None, None, None, None
            for i in self.Bagua.keys():
                if bengua_hugua_shang_num == self.Bagua[i]['先天卦数']:
                    bengua_shang_hugua = i
                    bengua_shang_hugua_code = eval(self.Bagua[i]['二进制'])
                if bengua_hugua_xia_num == self.Bagua[i]['先天卦数']:
                    bengua_xia_hugua = i
                    bengua_xia_hugua_code = eval(self.Bagua[i]['二进制'])
                if biangua_hugua_shang_num == self.Bagua[i]['先天卦数']:
                    biangua_shang_hugua = i
                    biangua_shang_hugua_code = eval(self.Bagua[i]['二进制'])
                if biangua_hugua_xia_num == self.Bagua[i]['先天卦数']:
                    biangua_xia_hugua = i
                    biangua_xia_hugua_code = eval(self.Bagua[i]['二进制'])
            hugua_code.append(bengua_shang_hugua_code)
            hugua_code.append(bengua_xia_hugua_code)
            hugua_code.append(biangua_shang_hugua_code)
            hugua_code.append(biangua_xia_hugua_code)
            hugua.append(bengua_shang_hugua)
            hugua.append(bengua_xia_hugua)
            hugua.append(biangua_shang_hugua)
            hugua.append(biangua_xia_hugua)
        # 求六十四卦
        bengua_hugua = None
        bengua_hugua_code = None
        biangua_hugua = None
        biangua_hugua_code = None
        for i in self.Liushisigua.keys():
            if self.Liushisigua[i]['上卦名'] == bengua_shang_hugua and self.Liushisigua[i]['下卦名'] == bengua_xia_hugua:
                bengua_hugua = i
                bengua_hugua_code = eval(self.Liushisigua[i]['二进制'])
            if self.Liushisigua[i]['上卦名'] == biangua_shang_hugua and self.Liushisigua[i][
                '下卦名'] == biangua_xia_hugua:
                biangua_hugua = i
                biangua_hugua_code = eval(self.Liushisigua[i]['二进制'])
        hugua.append(bengua_hugua)
        hugua.append(biangua_hugua)
        hugua_code.append(bengua_hugua_code)
        hugua_code.append(biangua_hugua_code)
        return hugua, hugua_code

    def qigua_guizang(self, guizangfangfa, gua_code, hugua_code):
        # 归藏入天盘中宫方法：
        # 1.四正（通用），四正归藏为上卦显示，四隅归藏为下卦不显示
        # 2.四隅，四隅归藏为上卦显示，四正归藏为下卦不显示？
        # 3.四正四隅，只有一个中宫卦
        # 4.本卦（元亨利贞排盘采用），本卦归藏为上卦显示，变卦归藏为下卦不显示
        # 5.四柱，？
        # 6.飞星，？
        # 7.用神，不予考虑
        if guizangfangfa == '四正':
            shanggua_code = (gua_code[0] ^ gua_code[1]) ^ (gua_code[2] ^ gua_code[3])  # 四正
            xiagua_code = (hugua_code[0] ^ hugua_code[1]) ^ (hugua_code[2] ^ hugua_code[3])
        elif guizangfangfa == '四隅':
            shanggua_code = (hugua_code[0] ^ hugua_code[1]) ^ (hugua_code[2] ^ hugua_code[3])  # 四隅
            xiagua_code = (gua_code[0] ^ gua_code[1]) ^ (gua_code[2] ^ gua_code[3])
        elif guizangfangfa == '四正四隅':
            shanggua_code = ((gua_code[0] ^ gua_code[1]) ^ (gua_code[2] ^ gua_code[3])) ^ ((hugua_code[0] ^ hugua_code[1]) ^ (hugua_code[2] ^ hugua_code[3]))
            xiagua_code = None
        elif guizangfangfa == '本卦':
            shanggua_code = (gua_code[0] ^ gua_code[1])  # 本卦
            xiagua_code = (gua_code[2] ^ gua_code[3])
        elif guizangfangfa == '四柱':  # 未完待续
            return ''
        elif guizangfangfa == '飞星':  # 未完待续
            return ''
        else:
            shanggua_code = None
            xiagua_code = None
        shanggua = None
        xiagua = None
        for i in self.Bagua.keys():
            if shanggua_code == eval(self.Bagua[i]['二进制']):
                shanggua = i
            if xiagua_code == eval(self.Bagua[i]['二进制']):
                xiagua = i
        # 求六十四卦
        gua = None
        gua_code = None
        for i in self.Liushisigua.keys():
            if self.Liushisigua[i]['上卦名'] == shanggua and self.Liushisigua[i]['下卦名'] == xiagua:
                gua = i
                gua_code = eval(self.Liushisigua[i]['二进制'])
        return [shanggua, xiagua, gua], [shanggua_code, xiagua_code, gua_code]
