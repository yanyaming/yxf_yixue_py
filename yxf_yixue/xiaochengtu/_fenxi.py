#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db2Cdata,Db


class Fenxi:
    def __init__(self):
        pass

    class Chuantongfenxi:
        def __init__(self):
            pass

        def fenxi(self, res, yonggong='中'):
            self.lunar = res['农历']
            self.ganzhi = res['干支']
            self.Bagua = res['八卦']
            self.Liushisigua = res['六十四卦']
            self.Pan = res['盘']
            self.dongyao = res['动爻']
            self.Fenxi = {'正推': {}, '触类': {}, '旁通': {}}
            self.zhengtuifa(yonggong)
            self.pangtongfa(yonggong)
            self.chuleifa(yonggong)

        def zhengtuifa(self, yonggong):
            # 从取用宫开始，看取用宫上是何卦，再推此卦宫上是何卦，直到不能推为止
            # 先找到用宫
            luogong = None
            luogong_gua = None
            for gong in self.Pan:
                if self.Pan[gong]['宫卦'] == yonggong:
                    luogong = int(self.Pan[gong]['宫数'])
                    luogong_gua = self.Pan[gong]['单卦']
            luogong_guagong = int(self.Bagua[luogong_gua]['后天卦数'])
            # 正推。有可能出现死循环，取最后一个
            tongji = {}  # 把正推过程中每一个出现的地盘宫记录进来，并统计出现次数，次数大于1即退出循环
            break_flag = 0
            while luogong != luogong_guagong:
                for value in tongji.values():
                    if value >= 2:
                        break_flag += 1
                if break_flag == 1:
                    break
                for gong in self.Pan:
                    if int(self.Pan[gong]['宫数']) == luogong_guagong:
                        if int(self.Pan[gong]['宫数']) not in tongji:
                            tongji[self.Pan[gong]['宫数']] = 1
                            luogong = int(self.Pan[gong]['宫数'])
                            luogong_gua = self.Pan[gong]['单卦']
                            luogong_guagong = int(self.Bagua[luogong_gua]['后天卦数'])
                        else:
                            if tongji[self.Pan[gong]['宫数']] == 1:
                                tongji[self.Pan[gong]['宫数']] += 1
                            break
            self.Fenxi['正推']['宫数'] = luogong
            self.Fenxi['正推']['宫卦'] = luogong_gua

        def pangtongfa(self, yonggong):
            # 举例： 占病,坎宫见乾,这个时候,旁推与乾卦相通的是坤, 所以要参看坤宫里有什么卦。
            # 旁通卦有两种取法,一种是取天盘的卦相通的卦宫, 一种是取地盘宫相通的卦宫,这个在使用的时候根据事情阴阳的不同而选择性使用。
            # 先找到用宫
            luogong_gua = None
            for gong in self.Pan:
                if self.Pan[gong]['宫卦'] == yonggong:
                    luogong_gua = self.Pan[gong]['单卦']
            # 旁通
            # 根据用宫卦判断旁通卦
            pangtong_gua = None
            if luogong_gua == '乾':
                pangtong_gua = '坤'
            if luogong_gua == '兑':
                pangtong_gua = '艮'
            if luogong_gua == '离':
                pangtong_gua = '坎'
            if luogong_gua == '震':
                pangtong_gua = '巽'
            if luogong_gua == '巽':
                pangtong_gua = '震'
            if luogong_gua == '坎':
                pangtong_gua = '离'
            if luogong_gua == '艮':
                pangtong_gua = '兑'
            if luogong_gua == '坤':
                pangtong_gua = '乾'
            tianpan_pangtonggong = []
            tianpan_pangtonggong_gua = []
            dipan_pangtonggong = []
            dipan_pangtonggong_gua = []
            for gong in self.Pan:
                if self.Pan[gong]['单卦'] == pangtong_gua:
                    tianpan_pangtonggong.append(self.Pan[gong]['宫数'])
                    tianpan_pangtonggong_gua.append(pangtong_gua)
                if self.Pan[gong]['宫数'] == int(self.Bagua[pangtong_gua]['后天卦数']):
                    dipan_pangtonggong.append(self.Pan[gong]['宫数'])
                    dipan_pangtonggong_gua.append(self.Pan[gong]['单卦'])
            self.Fenxi['旁通']['天通宫数'] = tianpan_pangtonggong
            self.Fenxi['旁通']['天通宫卦'] = tianpan_pangtonggong_gua
            self.Fenxi['旁通']['地通宫数'] = dipan_pangtonggong
            self.Fenxi['旁通']['地通宫卦'] = dipan_pangtonggong_gua

        def chuleifa(self, yonggong):
            # 触类法指的是取用宫里的卦，还出现在其它的宫里
            # 先找到用宫
            luogong_gua = None
            for gong in self.Pan:
                if self.Pan[gong]['宫卦'] == yonggong:
                    luogong_gua = self.Pan[gong]['单卦']
            # 触类
            chuleigong = []
            chuleigong_gua = []
            for gong in self.Pan:
                if self.Pan[gong]['单卦'] == luogong_gua:
                    chuleigong.append(self.Pan[gong]['宫数'])
                    chuleigong_gua.append(self.Pan[gong]['单卦'])
            self.Fenxi['触类']['宫数'] = chuleigong
            self.Fenxi['触类']['宫卦'] = chuleigong_gua

    # class CecaiFenxi:
    #     # 返回数字或数位
    #     def __init__(self):
    #         # 五行表
    #         self.wuxingName = '木 火 土 金 水'.split(' ')
    #         # 导入卦数据
    #         self.Com = InitData()
    #         self.Wuxing, self.Tiangan, self.Dizhi, self.Bagua, self.Liushisigua, self.Liushijiazi, self.Luoshu = self.Com.transform2db()
    #
    #     def cecaifenxi(self, dt, Info, Pan, yonggong='中'):
    #         self.lunar = dt[0]
    #         self.ganzhi = dt[1]
    #         self.Bagua = Info[0]
    #         self.Liushisigua = Info[1]
    #         self.Pan = Pan
    #         self.dongyao = Info[2]
    #         f = Fenxi().Chuantongfenxi()
    #         f.fenxi(dt, Info, Pan, yonggong=yonggong)
    #         self.Fenxi = f.Fenxi
    #
    #     def canwuyishufa(self):
    #         # 参伍倚数法
    #         # 整体求单一数
    #         bengua_shang = self.Pan['2']['单卦']
    #         bengua_xia = self.Pan['8']['单卦']
    #         biangua_shang = self.Pan['4']['单卦']
    #         biangua_xia = self.Pan['6']['单卦']
    #         bengua_shang_code = eval(self.Bagua[bengua_shang]['二进制'])
    #         bengua_xia_code = eval(self.Bagua[bengua_xia]['二进制'])
    #         num = []
    #         num.append(self.canwuyishufa_dangeshuzi(bengua_shang, bengua_xia, biangua_shang, biangua_xia))
    #         # 六个爻位纳数
    #         num1 = self.canwuyishufa_yaoweinashu(bengua_shang_code, bengua_xia_code)
    #         for i in num1:
    #             num.append(i)
    #         return num
    #
    #     def canwuyishufa_yaoweinashu(self, bengua_shang_code, bengua_xia_code):
    #         # 爻位纳数
    #         # 给本卦每一爻取对应的互卦，因为互卦没有动爻，所以互卦的变卦与互卦相同
    #         bengua_code = bengua_shang_code*8 + bengua_xia_code
    #         # 规则：
    #         # 初爻：561123
    #         # 二爻：612234
    #         # 三爻：123345
    #         # 四爻：234456
    #         # 五爻：345561
    #         # 六爻：456612
    #         code = []
    #         code.append(((bengua_code & 0b010000) >> 4) + ((bengua_code & 0b100000) >> 4) + ((bengua_code & 0b000001) << 2) +
    #                     ((bengua_code & 0b000001) << 3) + ((bengua_code & 0b000010) << 3) + ((bengua_code & 0b000100) << 3))
    #         code.append(((bengua_code & 0b100000) >> 5) + ((bengua_code & 0b000001) << 1) + ((bengua_code & 0b000010) << 1) +
    #                     ((bengua_code & 0b000010) << 2) + ((bengua_code & 0b000100) << 2) + ((bengua_code & 0b001000) << 2))
    #         code.append(((bengua_code & 0b000001) >> 0) + ((bengua_code & 0b000010) >> 0) + ((bengua_code & 0b000100) >> 0) +
    #                     ((bengua_code & 0b000100) << 1) + ((bengua_code & 0b001000) << 1) + ((bengua_code & 0b010000) << 1))
    #         code.append(((bengua_code & 0b000010) >> 1) + ((bengua_code & 0b000100) >> 1) + ((bengua_code & 0b001000) >> 1) +
    #                     ((bengua_code & 0b001000) << 0) + ((bengua_code & 0b010000) << 0) + ((bengua_code & 0b100000) << 0))
    #         code.append(((bengua_code & 0b000100) >> 2) + ((bengua_code & 0b001000) >> 2) + ((bengua_code & 0b010000) >> 2) +
    #                     ((bengua_code & 0b010000) >> 1) + ((bengua_code & 0b100000) >> 1) + ((bengua_code & 0b000001) << 5))
    #         code.append(((bengua_code & 0b001000) >> 3) + ((bengua_code & 0b010000) >> 3) + ((bengua_code & 0b100000) >> 3) +
    #                     ((bengua_code & 0b100000) >> 2) + ((bengua_code & 0b000001) << 4) + ((bengua_code & 0b000010) << 4))
    #         num = [0, 0, 0, 0, 0, 0]
    #         for i in range(0, 6):
    #             shang_code = code[i] // 8
    #             xia_code = code[i] % 8
    #             for j in self.Bagua.keys():
    #                 if shang_code == eval(self.Bagua[j]['二进制']):
    #                     shang = j
    #                 if xia_code == eval(self.Bagua[j]['二进制']):
    #                     xia = j
    #             num[i] = self.canwuyishufa_dangeshuzi(shang, xia, shang, xia)
    #         return num
    #
    #     def canwuyishufa_dangeshuzi(self, bengua_shang, bengua_xia, biangua_shang, biangua_xia):
    #         # 本卦定大组
    #         num = ''
    #         if self.Bagua[bengua_shang]['阴阳'] == self.Bagua[bengua_xia]['阴阳']:  # 阴阳得配
    #             if self.Bagua[bengua_shang]['升降'][0:1] == self.Bagua[bengua_xia]['升降'][0:1]:  # 外引或离心（上卦升）
    #                 num += '12345'
    #             else:
    #                 num += '67890'
    #         else:
    #             if self.Bagua[bengua_shang]['升降'][0:1] == self.Bagua[bengua_xia]['升降'][0:1]:  # 外引或离心（上卦升）
    #                 num += '13579'
    #             else:
    #                 num += '24680'
    #         # 定小组。可选判据：变卦上卦阴阳、动爻所在卦阴阳、世爻所在卦阴阳，此处选变卦上卦阴阳
    #         num1 = ''
    #         if self.Bagua[biangua_shang]['阴阳'] == '阳':
    #             for i in range(1, len(num), 2):
    #                 num1 += num[i:i+1]
    #         else:
    #             for i in range(0, len(num), 2):
    #                 num1 += num[i:i+1]
    #         # 定数。可选判据：变卦下卦、非动爻卦、非世爻卦，若剩余3个数则用三分法（上中下），剩余2个数用二分法（阴阳）
    #         num2 = ''
    #         if len(num1) == 2:
    #             if self.Bagua[biangua_xia]['阴阳'] == '阳':
    #                 num2 += num1[0:1]
    #             else:
    #                 num2 += num1[1:2]
    #         else:
    #             if self.Bagua[biangua_xia]['三分'] == '上':
    #                 num2 += num1[0:1]
    #             elif self.Bagua[biangua_xia]['三分'] == '中':
    #                 num2 += num1[1:2]
    #             else:
    #                 num2 += num1[2:3]
    #         return int(num2)
    #
    #     def dingweidanfa(self):
    #         # 卦-数-位对应：
    #         # 十位乾149
    #         # 百位坤850
    #         # 个位艮570
    #         # 个位兑429
    #         # 十位坎169
    #         # 十位离327
    #         # 百位震483
    #         # 百位巽538
    #         # 小成图分析：用宫-中宫；归藏方法-？；分析方法：中宫取组，正推法取数，旁通法定位
    #         # 中宫取组
    #         num = []
    #         zhonggonggua = self.Pan['5']['单卦']
    #         if zhonggonggua == '乾':
    #             num.append(1)
    #             num.append(4)
    #             num.append(9)
    #         if zhonggonggua == '坤':
    #             num.append(8)
    #             num.append(5)
    #             num.append(0)
    #         if zhonggonggua == '艮':
    #             num.append(5)
    #             num.append(7)
    #             num.append(0)
    #         if zhonggonggua == '兑':
    #             num.append(4)
    #             num.append(2)
    #             num.append(9)
    #         if zhonggonggua == '坎':
    #             num.append(1)
    #             num.append(6)
    #             num.append(9)
    #         if zhonggonggua == '离':
    #             num.append(3)
    #             num.append(2)
    #             num.append(7)
    #         if zhonggonggua == '震':
    #             num.append(4)
    #             num.append(8)
    #             num.append(3)
    #         if zhonggonggua == '巽':
    #             num.append(5)
    #             num.append(3)
    #             num.append(8)
    #         # 正推法取数
    #         # 判断阴阳月：阴月顺排（从上往下），阳月逆排（从下往上）
    #         # 三分法：
    #         # 乾艮兑：上
    #         # 坎离：  中
    #         # 坤震巽：下
    #         res = 0
    #         yue = self.ganzhi.split('：')[1].split(' ')[1][1:2]
    #         zhengtuigua = self.Fenxi['正推']['宫卦']
    #         if zhengtuigua in ['乾', '艮', '兑']:  # 上
    #             if yue in ['寅','辰','午','申','戌','子']:  # 逆排
    #                 res += num[2]
    #             else:
    #                 res += num[0]
    #         if zhengtuigua in ['坎', '离']:  # 中
    #             res += num[1]
    #         if zhengtuigua in ['坤', '震', '巽']:  # 下
    #             if yue in ['寅','辰','午','申','戌','子']:  # 逆排
    #                 res += num[0]
    #             else:
    #                 res += num[2]
    #         # 旁通法定位
    #         wei = ''
    #         try:
    #             pangtonggua_tian = self.Fenxi['旁通']['天通宫卦'][0]
    #             if pangtonggua_tian in ['坤','震', '巽']:  # 百
    #                 wei += '百'
    #             if pangtonggua_tian in ['乾','坎', '离']:  # 十
    #                 wei += '十'
    #             if pangtonggua_tian in ['艮','兑']:  # 个
    #                 wei += '个'
    #         except:
    #             pass
    #         try:
    #             pangtonggua_di = self.Fenxi['旁通']['地通宫卦'][0]
    #             if pangtonggua_di in ['坤','震', '巽']:  # 百
    #                 wei += '百'
    #             if pangtonggua_di in ['乾','坎', '离']:  # 十
    #                 wei += '十'
    #             if pangtonggua_di in ['艮','兑']:  # 个
    #                 wei += '个'
    #         except:
    #             pass
    #         return [res, wei]
