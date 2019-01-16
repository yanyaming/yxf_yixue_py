#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ..utils import Db, Db2Cdata


class Chuantongfenxi:
    def __init__(self):
        self.pan = None
        self.db = Db()
        self.db2cdata = Db2Cdata()

    def fenxi(self, pan):
        self.pan = pan
        pan['标签'] = '传统分析'
        return self.pan
