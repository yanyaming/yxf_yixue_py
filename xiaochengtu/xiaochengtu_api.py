# -*- coding: utf-8 -*-
import settings
import wannianli.wannianli_api
from xiaochengtu.paipan import Paipan
from xiaochengtu.fenxi import Fenxi


class Api:
    def __init__(self):
        self.p = None

    def paipan(self, datetime_obj, lingdongshu=None, shuziqigua=None, guizangfangfa='四正'):
        a = wannianli.wannianli_api.Api()
        self.p = Paipan()
        return_list = a.get_Calendar(datetime_obj)
        self.res = self.p.paipan(return_list[1], return_list[3], lingdongshu=lingdongshu, shuziqigua=shuziqigua, guizangfangfa=guizangfangfa)
        return self.res

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
        f.fenxi(self.res)
        return f.Fenxi

    # def get_canwuyishufa(self):
    #     if self.p is None:
    #         print('请先调用paipan()排盘后再使用本函数！')
    #         return None
    #     c = Fenxi().CecaiFenxi()
    #     c.cecaifenxi(self.dt, self.Info, self.Pan)
    #     res = c.canwuyishufa()
    #     return res
    #
    # def get_dingweidanfa(self):
    #     if self.p is None:
    #         print('请先调用paipan()排盘后再使用本函数！')
    #         return None
    #     c = Fenxi().CecaiFenxi()
    #     c.cecaifenxi(self.dt, self.Info, self.Pan)
    #     res = c.dingweidanfa()
    #     return res
