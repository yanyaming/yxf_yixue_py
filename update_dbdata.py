# -*- coding: utf-8 -*-
import settings
from utils.excel2db import Excel2Db


if __name__ == '__main__':
    c = Excel2Db()
    c.transform2db()
