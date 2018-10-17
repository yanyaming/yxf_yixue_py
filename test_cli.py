# -*- coding: utf-8 -*-
import settings
import os

"""
测试主入口:
"""


class Test:
    def __init__(self):
        while True:
            print('''
                #----------菜单----------#
                # 1.万年历               #
                # 2.八字                 #
                # 3.金口诀               #
                # 4.六爻                 #
                # 5.小成图               #
                # 6.退出                #
                ''')
            try:
                s1 = int(input("请选择："))
                if s1 == 1:
                    self.call("python wannianli/test_cli.py")
                elif s1 == 2:
                    self.call("python bazi/test_cli.py")
                elif s1 == 3:
                    self.call("python jinkoujue/test_cli.py")
                elif s1 == 4:
                    self.call("python liuyao/test_cli.py")
                elif s1 == 5:
                    self.call("python xiaochengtu/test_cli.py")
                elif s1 == 6:
                    break  # 跳出循环即结束整个程序
                    pass
            except:
                print("警告！您输入的不是有效数字！")
                pass

    @staticmethod
    def call(command):
        if settings.OS == 'Windows':
            os.system("cmd /k " + command)
        else:
            os.system(command)

if __name__ == '__main__':  # 程序入口
    Test()  # 调用主菜单
