#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3

"""
只在查询的时候连接数据库，查询完成后自动释放
注意：sql中的字符串数据用单引号，不能用双引号，所以在外部输入查询字符串要用双引号
使用sqlite3数据库保存易学通用数据
"""


class Db:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cdb.db'))
        self.cursor = self.conn.cursor()

    # 简单查询语句获取结果集，可根据条件筛选，中文的字段名需要用中括号括起来
    def select(self, tablename, column, condition=""):
        self.cursor.execute("SELECT {0} from {1} {2};".format(column, tablename, condition))
        rows = self.cursor.fetchall()
        return rows

    # 获取表的所有列名
    def get_colname(self, tablename):
        self.cursor.execute("PRAGMA table_info({0});".format(tablename))
        rows = self.cursor.fetchall()  # 每一行的内容是列信息
        colname = []
        for row in rows:
            colname.append(row[1])  # 第二个元素是列名
        return colname

    # 获取字典格式的列表，把每一行数据内容从值序列转化为键值对，得到的仍然是列表
    def get_tabledict_list(self, tablename):
        self.cursor.execute("PRAGMA table_info({0});".format(tablename))
        rows1 = self.cursor.fetchall()  # 每一行的内容是列信息
        colname = []
        for row in rows1:
            colname.append(row[1])  # 系统输出信息的第二个元素是列名
        self.cursor.execute("SELECT * from {0};".format(tablename))
        rows2 = self.cursor.fetchall()
        tabledict_list = []
        for row in rows2:
            dict_tmp = {}
            for i,col in enumerate(row):
                dict_tmp[colname[i]] = col
            tabledict_list.append(dict_tmp)
        return tabledict_list

    # 获取字典格式的列表，把每一行数据从值序列转化为键值对，并且用键索引（可节省大量搜索代码及执行时间）
    def get_tabledict_dict(self, tablename, key_col=1):  # 可指定索引键列
        self.cursor.execute("PRAGMA table_info({0});".format(tablename))
        rows1 = self.cursor.fetchall()  # 每一行的内容是列信息
        colname = []  # 存储列名的列表
        for row in rows1:
            colname.append(row[1])  # 系统输出信息的第二个元素是列名
        self.cursor.execute("SELECT * from {0};".format(tablename))
        rows2 = self.cursor.fetchall()
        tabledict_list = []  # 存储每行字典数据的列表
        for row in rows2:
            dict_tmp = {}
            for i,col in enumerate(row):
                dict_tmp[colname[i]] = col
                tabledict_list.append(dict_tmp)
        tabledict_dict = {}  # 给结果列表添加索引键（指定的索引键列的值必须唯一）
        keyname = colname[key_col]
        for i in tabledict_list:
            tabledict_dict.update({i[keyname]: i})
        return tabledict_dict

    # 直接执行SQL，但不立即提交；如果每一次插入都要立即提交会严重拖慢速度
    def execute(self, query_str):
        self.cursor.execute(query_str)
        rows = self.cursor.fetchall()
        return rows

    # 执行完修改数据库的SQL后提交事务
    def commit(self):
        self.conn.commit()
