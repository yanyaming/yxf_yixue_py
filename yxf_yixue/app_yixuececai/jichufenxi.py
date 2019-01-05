"""
列出总体与样本

    itertools说明：
        product 笛卡尔积　　（有放回抽样排列）
        permutations 排列　　（不放回抽样排列）
        combinations 组合,没有重复　　（不放回抽样组合）
        combinations_with_replacement 组合,有重复　　（有放回抽样组合）

"""

import itertools


def Pr(n, r, li=False):
    # 有放回排列
    n1 = []
    for i in range(0, n):
        n1.append(i)
    return_list = list(itertools.product(n1, repeat=r))
    count = len(return_list)
    if li is True:
        return count, return_list
    else:
        return count


def P(n, r, li=False):
    # 无放回排列
    n1 = []
    for i in range(0, n):
        n1.append(i)
    return_list = list(itertools.permutations(n1, r))
    count = len(return_list)
    if li is True:
        return count, return_list
    else:
        return count


def Cr(n, r, li=False):
    # 有放回组合
    n1 = []
    for i in range(0, n):
        n1.append(i)
    return_list = list(itertools.combinations_with_replacement(n1, r))
    count = len(return_list)
    if li is True:
        return count, return_list
    else:
        return count


def C(n, r, li=False):
    # 无放回组合
    n1 = []
    for i in range(0, n):
        n1.append(i)
    return_list = list(itertools.combinations(n1, r))
    count = len(return_list)
    if li is True:
        return count, return_list
    else:
        return count


class Pailiexing:
    # 福彩3D、排列三，有排列型
    def __init__(self):
        self.Prk = Pr(10, 3, True)[1]  # 考虑排三直选
        self.Pk = P(10, 3, True)[1]  # 不考虑排三直选
        self.Crk = Cr(10, 3, True)[1]  # 考虑排三组选
        self.Ck = C(10, 3, True)[1]  # 不考虑排三组选

    def lilungailv(self):
        print('理论概率分析基于直选开奖，直选开奖才是本质')
        self.daxiaojiou()
        self.hezhi()
        self.lianhao()

    def daxiaojiou(self):
        Prk_duizhao = self.Prk.copy()
        Prk_kebian = self.Prk.copy()
        # 大小奇偶
        for i in Prk_duizhao:
            xiao = 0
            ji = 0
            for j in range(0, 3):
                if i[j] in [0, 1, 2, 3, 4]:
                    xiao += 1
                if i[j] in [1, 3, 5, 7, 9]:
                    ji += 1
            if ji == 3:  # 全奇
                if i in Prk_kebian:
                    Prk_kebian.remove(i)
        gailv = (len(Prk_duizhao) - len(Prk_kebian))/len(Prk_duizhao)
        print('大小奇偶[全奇or全偶or全小or全大]概率：'+str(gailv))

    def hezhi(self):
        Prk_duizhao = self.Prk.copy()
        Prk_kebian = self.Prk.copy()
        # 和值
        for i in Prk_duizhao:
            he = i[0]+i[1]+i[2]
            if he in [0,1,2,3,4,5,6,27,26,25,24,23,22,21]:  # 0:0.1%, 1:0.3%, 2:0.6%, 3:1%, 4:1.5%, 5:2.1%, 6:2.8%
                if i in Prk_kebian:
                    Prk_kebian.remove(i)
        gailv = (len(Prk_duizhao) - len(Prk_kebian)) / len(Prk_duizhao)
        print('和值[0-6，21-27]概率：' + str(gailv))

    def lianhao(self):
        Prk_duizhao = self.Prk.copy()
        Prk_kebian = self.Prk.copy()
        # 连号
        for j in Prk_duizhao:
            # 间隔1连号前8组
            if (j[2] - j[1]) == 1 and (j[1] - j[0]) == 1:
                if j in Prk_kebian:
                    Prk_kebian.remove(j)
            # 间隔2连号前6组
            elif (j[2] - j[1]) == 2 and (j[1] - j[0]) == 2:
                if j in Prk_kebian:
                    Prk_kebian.remove(j)
        # 间隔1循环连号
        if [0, 8, 9] in Prk_kebian:
            Prk_kebian.remove([0, 8, 9])  # 直接杀掉特定的组
        if [0, 1, 9] in Prk_kebian:
            Prk_kebian.remove([0, 1, 9])
        # 间隔2循环连号
        if [0, 6, 8] in Prk_kebian:
            Prk_kebian.remove([0, 6, 8])
        if [1, 7, 9] in Prk_kebian:
            Prk_kebian.remove([1, 7, 9])
        if [0, 2, 8] in Prk_kebian:
            Prk_kebian.remove([0, 2, 8])
        if [1, 3, 9] in Prk_kebian:
            Prk_kebian.remove([1, 3, 9])
        gailv = (len(Prk_duizhao) - len(Prk_kebian)) / len(Prk_duizhao)
        print('连号[单步连号，二步连号，循环连号]概率：' + str(gailv))


class Letouxing:
    # 双色球、大乐透、七乐彩等无排列型
    def __init__(self):
        pass

