# -*- coding: utf-8 -*-
import settings
import os
import sys
import datetime
from utils.code2excel import Code2Excel
from utils.excel2db import Excel2Db
from utils.db import Db
from utils.db2cdata import Db2Cdata


if __name__ == '__main__':
    # c = Db2Cdata()
    # print(c.get_wuxing_shengke('木','金'))
    # print(c.get_wuxing_shishen('乙'))
    # # d = Db()
    # # print(d.get_tabledict_dict('[基础表-六十甲子]'))
    e = Excel2Db()
    e.read_excel(os.path.join(settings.BASE_DIR, os.path.join("utils", "cexcel")),'关联表-五行十二长生运.xlsx')
    pass
