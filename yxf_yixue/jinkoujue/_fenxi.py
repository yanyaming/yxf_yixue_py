#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db, Db2Cdata


class Chuantongfenxi:
    def __init__(self):
        self.zhanshi = None
        self.pan = None
        self.ke = None
        self.db = Db()
        self.db2cdata = Db2Cdata()

    def fenxi(self, zhanshi, pan, ke):
        self.zhanshi = zhanshi
        self.pan = pan
        self.ke = ke
        pan['标签'] = '传统分析'
        return [self.zhanshi, self.pan, self.ke]


class Lianghuafenxi(Chuantongfenxi):
    def __init__(self):
        super(Lianghuafenxi, self).__init__()
        self.zhanshi = None
        self.pan = None
        self.ke = None
        self.db = Db()
        self.db2cdata = Db2Cdata()

    def fenxi(self, zhanshi, pan, ke):
        self.zhanshi = zhanshi
        self.pan = pan
        self.ke = ke
        pan['标签'] = '量化分析'
        return [self.zhanshi, self.pan, self.ke]
