#!/usr/bin/python3
# -*- coding: utf-8 -*-


# 本代码是直接手动执行的，不需要被其他代码使用
if __name__ == '__main__':
    from utils import Excel2Db  # 在当前路径直接执行不能加点号
    c = Excel2Db()
    c.transform2db()
