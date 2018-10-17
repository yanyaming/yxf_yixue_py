# -*- coding: utf-8 -*-
import settings
from utils.db import Db


class Db2Cdata:
    def __init__(self):
        self.db = Db()
        self.Wuxing = self.db.get_tabledict_dict("[基础表-五行]")
        self.Tiangan = self.db.get_tabledict_dict("[基础表-十天干]")
        self.Dizhi = self.db.get_tabledict_dict("[基础表-十二地支]")
        self.Bagua = self.db.get_tabledict_dict("[基础表-八卦]")

    def get_wuxing_shengke(self, input_x, input_y=None, return_type='耗'):
        # 输入五行，返回对输入五行起对应作用的五行（返回类型通过return_type指定）；或者输入两个五行，返回后一个对前一个的作用关系
        # 生：生我、印枭、父母；助：同我、比劫、兄弟；克：克我、官杀、官鬼；泄：我生、食伤、子女；耗：我克、财星、妻财
        Wuxing = self.Wuxing.copy()
        # 获取输入五行的序号（1-5）
        wuxingIdx = int(Wuxing[input_x]['序号'])
        # 根据输入五行序号计算生助克泄耗的五行序号
        haoIdx = wuxingIdx + 2
        if haoIdx > 5:
            haoIdx -= 5
        keIdx = wuxingIdx - 2
        if keIdx < 1:
            keIdx += 5
        shengIdx = wuxingIdx - 1
        if shengIdx < 1:
            shengIdx += 5
        zhuIdx = wuxingIdx
        xieIdx = wuxingIdx + 1
        if xieIdx > 5:
            xieIdx -= 5
        # 五行生克
        for i in Wuxing.values():
            if int(i['序号']) == haoIdx:
                i['生克'] = '耗'
            if int(i['序号']) == keIdx:
                i['生克'] = '克'
            if int(i['序号']) == shengIdx:
                i['生克'] = '生'
            if int(i['序号']) == zhuIdx:
                i['生克'] = '助'
            if int(i['序号']) == xieIdx:
                i['生克'] = '泄'
        if input_y is None:
            for i in Wuxing.values():
                if i['生克'] == return_type:
                    return i['五行']
        else:
            return Wuxing[input_y]['生克']

    def get_wuxing_shishen(self, input_x, return_type='正财'):
        # 输入五行、天干、地支、八卦，通过本函数自动判断，返回对应生克关系的五行、天干、地支、八卦，输入什么类型就返回什么类型
        # 要考虑阴阳异同，所以参数使用八字六亲
        # 其中五行本身无阴阳之分，在输入时第一个字符添加阴阳，返回值同理；八卦某五行只有一个则不管正偏均返回
        Wuxing = self.Wuxing.copy()
        Tiangan = self.Tiangan.copy()
        Dizhi = self.Dizhi.copy()
        Bagua = self.Bagua.copy()
        # 输入五行的判断逻辑，如：阴金
        if input_x[1:2] in self.Wuxing.keys():
            yinyang = input_x[0:1]
            caixing = self.get_wuxing_shengke(input_x[1:2], return_type='耗')
            guansha = self.get_wuxing_shengke(input_x[1:2], return_type='克')
            yinxiao = self.get_wuxing_shengke(input_x[1:2], return_type='生')
            bijie = input_x[1:2]
            shishang = self.get_wuxing_shengke(input_x[1:2], return_type='泄')
            Wuxing[caixing]['六亲'] = '正财偏财'  # 前为异性，后为同性
            Wuxing[guansha]['六亲'] = '正官七杀'
            Wuxing[yinxiao]['六亲'] = '正印偏印'
            Wuxing[bijie]['六亲'] = '劫财比肩'
            Wuxing[shishang]['六亲'] = '伤官食神'
            for i in Wuxing.values():
                if i['六亲'][0:2] == return_type:
                    if yinyang == '阴':
                        return '阳' + i['五行']
                    else:
                        return '阴' + i['五行']
                if i['六亲'][2:4] == return_type:
                    if yinyang == '阴':
                        return '阴' + i['五行']
                    else:
                        return '阳' + i['五行']
        # 输入天干的判断逻辑，如：甲
        if input_x in self.Tiangan.keys():
            wuxing = Tiangan[input_x]['五行']
            yinyang = Tiangan[input_x]['阴阳']
            caixing = self.get_wuxing_shengke(wuxing, return_type='耗')
            guansha = self.get_wuxing_shengke(wuxing, return_type='克')
            yinxiao = self.get_wuxing_shengke(wuxing, return_type='生')
            bijie = wuxing
            shishang = self.get_wuxing_shengke(wuxing, return_type='泄')
            for i in Tiangan.values():
                if i['五行'] == caixing:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '偏财'
                    else:
                        i['六亲'] = '正财'
                if i['五行'] == guansha:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '七杀'
                    else:
                        i['六亲'] = '正官'
                if i['五行'] == yinxiao:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '偏印'
                    else:
                        i['六亲'] = '正印'
                if i['五行'] == bijie:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '比肩'
                    else:
                        i['六亲'] = '劫财'
                if i['五行'] == shishang:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '食神'
                    else:
                        i['六亲'] = '伤官'
            for i in Tiangan.values():
                if i['六亲'] == return_type:
                    return i['天干']
        # 输入地支的判断逻辑，如：寅（土地支只返回辰代表阳、丑代表阴）
        if input_x in self.Dizhi.keys():
            wuxing = Dizhi[input_x]['五行']
            yinyang = Dizhi[input_x]['阴阳']
            caixing = self.get_wuxing_shengke(wuxing, return_type='耗')
            guansha = self.get_wuxing_shengke(wuxing, return_type='克')
            yinxiao = self.get_wuxing_shengke(wuxing, return_type='生')
            bijie = wuxing
            shishang = self.get_wuxing_shengke(wuxing, return_type='泄')
            for i in Dizhi.values():
                if i['五行'] == caixing:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '偏财'
                    else:
                        i['六亲'] = '正财'
                if i['五行'] == guansha:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '七杀'
                    else:
                        i['六亲'] = '正官'
                if i['五行'] == yinxiao:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '偏印'
                    else:
                        i['六亲'] = '正印'
                if i['五行'] == bijie:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '比肩'
                    else:
                        i['六亲'] = '劫财'
                if i['五行'] == shishang:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '食神'
                    else:
                        i['六亲'] = '伤官'
            for i in Dizhi.values():
                if i['六亲'] == return_type:
                    return i['地支']
        # 输入八卦的判断逻辑，如：乾（有些情况正偏可能为同一个值）
        if input_x in self.Bagua.keys():
            wuxing = Bagua[input_x]['五行']
            yinyang = Bagua[input_x]['阴阳']
            caixing = self.get_wuxing_shengke(wuxing, return_type='耗')
            guansha = self.get_wuxing_shengke(wuxing, return_type='克')
            yinxiao = self.get_wuxing_shengke(wuxing, return_type='生')
            bijie = wuxing
            shishang = self.get_wuxing_shengke(wuxing, return_type='泄')
            Wuxing[caixing]['六亲'] = '正财偏财'  # 前为异性，后为同性
            Wuxing[guansha]['六亲'] = '正官七杀'
            Wuxing[yinxiao]['六亲'] = '正印偏印'
            Wuxing[bijie]['六亲'] = '劫财比肩'
            Wuxing[shishang]['六亲'] = '伤官食神'
            for i in Bagua.values():
                if i['五行'] == caixing:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '偏财'
                    else:
                        i['六亲'] = '正财'
                if i['五行'] == guansha:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '七杀'
                    else:
                        i['六亲'] = '正官'
                if i['五行'] == yinxiao:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '偏印'
                    else:
                        i['六亲'] = '正印'
                if i['五行'] == bijie:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '比肩'
                    else:
                        i['六亲'] = '劫财'
                if i['五行'] == shishang:
                    if i['阴阳'] == yinyang:
                        i['六亲'] = '食神'
                    else:
                        i['六亲'] = '伤官'
            # 先确定应当返回的五行
            return_wuxing = None
            for i in Wuxing.values():
                if return_type in i['六亲']:
                    return_wuxing = i['五行']
            # 再统计本五行的八卦个数
            return_bagua_list = []
            for i in Bagua.values():
                if i['五行'] == return_wuxing:
                    return_bagua_list.append(i)
            # 如果有两个，则按正偏返回，如果只有一个，则立即返回
            if len(return_bagua_list) == 2:
                for i in return_bagua_list:
                    if i['六亲'] == return_type:
                        return i['卦名']
            else:
                return return_bagua_list[0]['卦名']
