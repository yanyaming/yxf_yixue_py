from utils.excel2db import InitData


class Dulicecai:
    # 返回数字或数位
    def __init__(self):
        self.Com = InitData()
        self.Wuxing, self.Tiangan, self.Dizhi, self.Bagua, self.Liushisigua, self.Liushijiazi, self.Luoshu = self.Com.transform2db()

    def cecaifenxi(self, ganzhi, Info, Pan):
        self.ganzhi = ganzhi
        self.Info = Info
        self.Bazi = Pan

    def wuxingheyifa(self, shuziqigua):
        # 五行合一法
        # 输入前3为福彩3D奖号，后3为排列三奖号
        # 求归藏卦
        gua = self.wuxingheyifa_guizang(shuziqigua)
        shu = []
        # 求卦的五行、阴阳
        wuxing = self.Bagua[gua]['五行']
        yinyang = self.Bagua[gua]['阴阳']
        # 求生出之五行
        gua_sheng_wuxing = self.Com.get_wuxing_shengke(wuxing, return_type='泄')
        if yinyang == '阴':  # 如果原阴阳是阴，则取生出五行的阳，五行数第一位是阳数
            shu.append(self.Wuxing[gua_sheng_wuxing]['五行数']//10)
        else:
            shu.append(self.Wuxing[gua_sheng_wuxing]['五行数']%10)
        # 另外参考开奖号本身的五行，有相同码或同五行码，则取生出的五行（阴阳暂时不判断）
        for i in self.Wuxing.keys():
            self.Wuxing[i]['次数'] = 0
        for i in shuziqigua:
            if i in [3, 8]:
                self.Wuxing['木']['次数'] += 1
            if i in [7, 2]:
                self.Wuxing['火']['次数'] += 1
            if i in [5, 0]:
                self.Wuxing['土']['次数'] += 1
            if i in [9, 4]:
                self.Wuxing['金']['次数'] += 1
            if i in [1, 6]:
                self.Wuxing['水']['次数'] += 1
        for i in self.Wuxing.keys():
            if self.Wuxing[i]['次数'] > 1:
                sheng_wuxing = self.Com.get_wuxing_shengke(i, return_type='泄')
                shu.append(self.Wuxing[sheng_wuxing]['五行数']//10)
                shu.append(self.Wuxing[sheng_wuxing]['五行数']%10)
        return shu

    def wuxingheyifa_guizang(self, shuziqigua):
        # 从输入的数字求卦
        num = [0, 0, 0, 0, 0, 0]
        gua = []
        # 数值计算，除8取余
        for i in range(0, 6):
            num[i] += shuziqigua[i] % 8
            if num[i] == 0:
                num[i] += 8
        # 由数字依照先天卦数取卦
        for i in self.Bagua.keys():
            for j in num:
                if j == self.Bagua[i]['先天卦数']:
                    gua.append(i)
        # 统计每个卦出现的次数
        tongji = {}
        for i in gua:
            if i not in tongji:
                tongji[i] = 1
            else:
                tongji[i] += 1
        # 删除有重复的卦和坤卦
        for i in tongji.keys():
            if tongji[i] == 2 or tongji[i] == 3:
                gua.remove(i)
                gua.remove(i)
            if tongji[i] == 4 or tongji[i] == 5:
                gua.remove(i)
                gua.remove(i)
                gua.remove(i)
                gua.remove(i)
            if tongji[i] == 6:
                gua.remove(i)
                gua.remove(i)
                gua.remove(i)
                gua.remove(i)
                gua.remove(i)
                gua.remove(i)
                gua.append('坤')
        for i in gua:
            if len(gua) != 1:
                if i == '坤':
                    gua.remove(i)
        # 以剩余的卦为基础，求二进制代码，进行异或运算（归藏操作）
        gua_code = []
        for i in self.Bagua.keys():
            for j in gua:
                if j == i:
                    gua_code.append(eval(self.Bagua[i]['二进制']))
        res = 0  # 与0异或值不变
        for i in gua_code:
            if i == 0:
                res = i
            else:
                res = res ^ i
        # 异或运算完成后，由二进制代码查询对应的卦
        res_gua = None
        for i in self.Bagua.keys():
            if res == eval(self.Bagua[i]['二进制']):
                res_gua = i
        return res_gua

    def hezhiwuxingshahaofa(self, a_hewei, b_hewei, c_hewei):
        # 和值五行杀号法
        # 原方法有马后炮和牵强附会的嫌疑
        # 输入为前3期的和值尾，a为前3，b为前2，c为前1
        a = {'和尾': a_hewei}
        b = {'和尾': b_hewei}
        c = {'和尾': c_hewei}
        # 判断5、0之外的数
        for i in self.Luoshu.keys():
            if i == 5:
                continue
            if a['和尾'] == i:
                a['五行'] = self.Luoshu[i]['宫五行']
                a['阴阳'] = self.Luoshu[i]['宫阴阳']
                a['和值'] = self.Luoshu[i]['和值']
            if b['和尾'] == i:
                b['五行'] = self.Luoshu[i]['宫五行']
                b['阴阳'] = self.Luoshu[i]['宫阴阳']
                b['和值'] = self.Luoshu[i]['和值']
            if c['和尾'] == i:
                c['五行'] = self.Luoshu[i]['宫五行']
                c['阴阳'] = self.Luoshu[i]['宫阴阳']
                c['和值'] = self.Luoshu[i]['和值']
        # 单独判断5、0
        if a['和尾'] in [5, 0]:
            a['五行'] = '土'
            if a['和尾'] == 5:
                a['阴阳'] = '阳'
                a['和值'] = 9
            else:
                a['阴阳'] = '阴'
                a['和值'] = 6
        if b['和尾'] in [5, 0]:
            b['五行'] = '土'
            if b['和尾'] == 5:
                b['阴阳'] = '阳'
                b['和值'] = 9
            else:
                b['阴阳'] = '阴'
                b['和值'] = 6
        if c['和尾'] in [5, 0]:
            c['五行'] = '土'
            if c['和尾'] == 5:
                c['阴阳'] = '阳'
                c['和值'] = 9
            else:
                c['阴阳'] = '阴'
                c['和值'] = 6
        # 在此处加入有重复五行且有土五行的约束条件
        if a['五行'] == b['五行'] or a['五行'] == c['五行'] or b['五行'] == c['五行']:
            # 统计土五行出现的次数
            tongji_tu = 0
            for i in [a['五行'], b['五行'], c['五行']]:
                if i == '土':
                    tongji_tu += 1
            # 两土的情况：强对强，弱对弱，两土需与另一五行化成同一强弱
            if tongji_tu == 2:
                for i in [a, b, c]:
                    if i['五行'] != '土':
                        if i['阴阳'] == '阳':  # 如果另一五行为强
                            for j in [a, b, c]:
                                if j['五行'] == '土':
                                    j['和值'] = 9  # 两个土均化为强土
                        else:  # 如果另一五行为弱
                            for j in [a, b, c]:
                                if j['五行'] == '土':
                                    j['和值'] = 6  # 两个土均化为弱土
            # 一土的情况：强对强，弱对弱，另一五行需与一土化成同一强弱
            if tongji_tu == 1:
                for i in [a, b, c]:
                    if i['五行'] == '土':
                        if i['阴阳'] == '阳':  # 如果土为强
                            for j in [a, b, c]:
                                if j['五行'] == '水':
                                    j['和值'] = 27  # 另一五行均化为强
                                if j['五行'] == '火':
                                    j['和值'] = 24  # 另一五行均化为强
                        else:  # 如果土为弱
                            for j in [a, b, c]:
                                if j['五行'] == '水':
                                    j['和值'] = 21  # 另一五行均化为弱
                                if j['五行'] == '火':
                                    j['和值'] = 18  # 另一五行均化为弱
        # 从上到下
        a['生克'] = self.Com.get_wuxing_shengke(b['五行'], a['五行'])  # 后一个对前一个的作用关系
        b['生克'] = self.Com.get_wuxing_shengke(c['五行'], b['五行'])
        c['生克'] = self.Com.get_wuxing_shengke(a['五行'], c['五行'])
        # 计算基本结果
        # 上一个对下一个：生、助为生，取加法；克、泄、耗为克，取减法，其中泄、耗为反克，需添加修正值1
        num = 0
        if a['生克'] in ['生', '助']:  # 方法中所说的生
            num += a['和值'] + b['和值']
        elif a['生克'] in ['克']:  # 方法中所说的克
            num += a['和值'] - b['和值']
        elif a['生克'] in ['泄', '耗']:  # 方法中所说的反克
            num += a['和值'] - b['和值'] + 1
        if b['生克'] in ['生', '助']:
            num += b['和值'] + c['和值']
        elif b['生克'] in ['克']:
            num += b['和值'] - c['和值']
        elif b['生克'] in ['泄', '耗']:
            num += b['和值'] - c['和值'] + 1
        if c['生克'] in ['生', '助']:
            num += c['和值'] + a['和值']
        elif c['生克'] in ['克']:
            num += c['和值'] - a['和值']
        elif c['生克'] in ['泄', '耗']:
            num += c['和值'] - a['和值'] + 1
        # 附加计算，是否对计算结果求位和，添加修正值等
        num2 = 0
        # 不求位和的条件：1.无反克；2.有重复五行
        if (a['生克'] not in ['泄', '耗'] and b['生克'] not in ['泄', '耗'] and c['生克'] not in ['泄', '耗']) \
                or (a['五行'] == b['五行'] or a['五行'] == c['五行'] or b['五行'] == c['五行']):
            num2 += num
            # 统计各五行出现的次数
            tongji_jin = 0
            tongji_mu = 0
            for i in [a['五行'], b['五行'], c['五行']]:
                if i == '金':
                    tongji_jin += 1
                if i == '木':
                    tongji_mu += 1
            # 以下是对基本计算结果的修正
            # 两金的情况：两金数相加，另一关系生则加，克则减
            if tongji_jin == 2:
                for i in [a, b, c]:
                    if i['五行'] != '金':
                        if i['生克'] in ['生', '助']:
                            num2 = 24 + 24 + a['和值']
                        elif i['生克'] in ['克']:
                            num2 = 24 + 24 - a['和值']
                        elif i['生克'] in ['泄', '耗']:
                            num2 = 24 + 24 - a['和值'] + 1
            # 两木的情况：两木数相加，另一关系生则加，克则减
            if tongji_mu == 2:
                for i in [a, b, c]:
                    if i['五行'] != '木':
                        if i['生克'] in ['生', '助']:
                            num2 = 21 + 21 + a['和值']
                        elif i['生克'] in ['克']:
                            num2 = 21 + 21 - a['和值']
                        elif i['生克'] in ['泄', '耗']:
                            num2 = 21 + 21 - a['和值'] + 1
        # 一般情况下，要求计算结果的位和
        else:
            num2 = num // 100 + num // 10 + num % 10
            # 过百修正
            if num >= 100:
                # 若为两生一克的情况则不添加修正值（未完待续）
                tongji_sheng = 0
                for i in [a, b, c]:
                    if i['生克'] in ['生', '助']:
                        tongji_sheng += 1
                # 小半月型不添加修正值？暂时不采用
                if 0:
                    pass
                # 一般情况下需添加修正值2
                else:
                    num2 += 2
        num_str = str(num2)
        # 最终结果每一位扩展+-1，3-6个数字，个别3位数的情况数字会更多
        res = []
        for i in range(0, len(num_str)):
            if int(num_str[i]) - 1 < 0:
                if int(num_str[i]) - 1 + 10 not in res:
                    res.append(int(num_str[i]) - 1 + 10)
            else:
                if int(num_str[i]) - 1 not in res:
                    res.append(int(num_str[i]) - 1)
            if int(num_str[i]) not in res:
                res.append(int(num_str[i]))
            if int(num_str[i]) + 1 > 9:
                if int(num_str[i]) + 1 - 10 not in res:
                    res.append(int(num_str[i]) + 1 - 10)
            else:
                if int(num_str[i]) + 1 not in res:
                    res.append(int(num_str[i]) + 1)
        return res

    def baguawuxingshufa(self, shijihao, kaijianghao):
        pass
