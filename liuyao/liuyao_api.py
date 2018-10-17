# -*- coding: utf-8 -*-
import settings
import wannianli.wannianli_api
from liuyao.paipan import Paipan
from liuyao.fenxi import Fenxi


class Api:
    def __init__(self):
        self.p = None

    def paipan(self, datetime_obj, qiguafangfa='标准时间起卦', qiguashuru=None, naganzhifangfa='传统京氏'):
        a = wannianli.wannianli_api.Api()
        self.p = Paipan()
        return_list = a.get_Calendar(datetime_obj)
        res = self.p.paipan(return_list[1], return_list[3], qiguafangfa=qiguafangfa, qiguashuru=qiguashuru, naganzhifangfa=naganzhifangfa)
        return res

    def print_pan(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        self.p.output()

    def get_chuantongfenxi(self):
        if self.p is None:
            print('请先调用paipan()排盘后再使用本函数！')
            return None
        f = Fenxi().Chuantongfenxi()
        s = f.fenxi(self.dt, self.Info, self.Pan)
        return s

    # def get_danqishikongfa(self, dt, qiguashuru):
    #     # 起卦输入是某位的数值转化成的爻位
    #     a = wannianli.wannianli_api.Api()
    #     self.p = Paipan()
    #     return_list = a.get_Calendar(dt)
    #     self.dt, self.Info, self.Pan = self.p.paipan(return_list[1], return_list[3], qiguafangfa='输入动爻时间起卦', qiguashuru=[qiguashuru])
    #     c = Fenxi().CecaiFenxi()
    #     c.cecaifenxi(self.dt, self.Info, self.Pan)
    #     # 解卦
    #     res = c.danqishikongfa(qiguashuru)
    #     return res
    #
    # def get_chunshijianguafa(self, dt, qiguashuru):
    #     # 起卦输入是期号尾数
    #     a = wannianli.wannianli_api.Api()
    #     self.p = Paipan()
    #     return_list = a.get_Calendar(dt)
    #     self.dt, self.Info, self.Pan = self.p.paipan(return_list[1], return_list[3], qiguafangfa='标准时间起卦', qiguashuru=qiguashuru)
    #     c = Fenxi().CecaiFenxi()
    #     c.cecaifenxi(self.dt, self.Info, self.Pan)
    #     # 解卦
    #     res = c.chunshijianguafa()
    #     return res
