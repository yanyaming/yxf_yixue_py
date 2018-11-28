#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Chuantongfenxi:
    def __init__(self):
        self.pan = None

    def fenxi(self, pan):
        self.pan = pan
        pan['标签'] = '传统分析'
        return self.pan

    def wangshuai(self):
        # 不通过量化，而是通过特定的组合直接判断
        pass

    def geju(self):
        pass

    def yongshen(self):
        pass

    def wuxingqushu(self):
        pass

    def output_addition(self):
        map_str = ''
        map_str += '\n\n【传统分析】\n'
        map_str += '五行力量：'
        map_str += '\n'
        map_str += '六亲力量：'
        map_str += '\n'
        map_str += '十神力量：'
        map_str += '\n'
        map_str += '日主强弱：'
        map_str += '\n'
        map_str += '八字格局：'
        map_str += '\n'
        map_str += '八字喜忌：'
        map_str += '\n'
        map_str += '建议取用：'
        map_str += '\n'
        map_str += '建议取数：'
        return map_str


class Lianghuafenxi(Chuantongfenxi):
    def __init__(self):
        super(Lianghuafenxi, self).__init__()

    def fenxi(self, pan):
        self.pan = pan
        pan['标签'] = '量化分析'
        return self.pan

    def wangshuai(self):
        # 此处采用新浪博客“留指爪”的方法，原文没有提及五行自身旺衰的变化，我认为需要添加此逻辑
        self.pan['量化分析']['五行'] = self.pan['五行']  # 存储五行（六亲）量化值
        self.pan['量化分析']['天干'] = self.pan['天干']  # 后面会把所有地支转化为天干，存储十神量化值
        # 八字配比
        # 年日时干支、月干均为0.5，月支1.5，共5，最终归一化到1。每次计算后都要做归一化处理

        # 五行自身旺衰（依月支）
        # 同我旺1.5，生我相1.2，我生休0.7，我克囚0.6，克我死0.3

        # 日元力量得分
        # 生助
        # 克泄耗
        # 阴气
        # 阳气
        pass

    def geju(self):
        pass

    def yongshen(self):
        pass

    def wuxingqushu(self):
        pass

    def output_addition(self):
        map_str = ''
        map_str += '\n\n【量化分析】\n'
        map_str += '五行力量：'
        map_str += '\n'
        map_str += '六亲力量：'
        map_str += '\n'
        map_str += '十神力量：'
        map_str += '\n'
        map_str += '日主强弱：'
        map_str += '\n'
        map_str += '八字格局：'
        map_str += '\n'
        map_str += '八字喜忌：'
        map_str += '\n'
        map_str += '建议取用：'
        map_str += '\n'
        map_str += '建议取数：'
        return map_str
