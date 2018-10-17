# build-in
import os  # 系统命令
import sys  # python设置
import shutil  # 高级文件操作
import timeit  # 计时相关
from datetime import datetime  # 日期时间
import time  # 时间相关
import random

# init
sys.path.append(os.getcwd())  # 添加工程根目录(yixue_py3_yxf)到path环境变量

# module
import yixuececai.datax as datax
import yixuececai.huiguifenxi as huiguifenxi
import yixuececai.yuce as yuce
import yixuececai.fenxi as fenxi
import yixuececai.dulicecai as dulicecai
import yixuececai.kexingxingyanjiu as kexingxingyanjiu
from yixuececai.fenxi import Pr
from yixuececai.fenxi import P
from yixuececai.fenxi import C
from yixuececai.fenxi import Cr


class Cli:
    def __init__(self):
        print("===== 初始化工作目录 =====")
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        print("基础路径：", BASE_DIR)
        os.chdir(BASE_DIR)  # 进入基础路径
        print("===== 开始工作 =====")
        try:  # 调用work()进入工作，直到工作完成
            self.work()
            print('===== 工作成功。 =====')
        except Exception as e:
            print('===== 工作失败。 =====')
            raise e
        finally:
            print("结束。")

    def work(self):
        while True:
            print('''
                #---------易学测彩菜单----------#
                # 1.数据处理                    #
                # 2.回归分析                    #
                # 3.可行性研究                  #
                # 4.投注分析                    #
                # 5.综合预测                    #
                # 6.返回
                ''')
            try:
                s1 = int(input("请选择："))
                if s1 == 1:
                    self.work1()
                    pass
                elif s1 == 2:
                    self.work2()
                    pass
                elif s1 == 3:
                    self.work3()
                    pass
                elif s1 == 4:
                    self.work4()
                    pass
                elif s1 == 5:
                    self.work5()
                    pass
                elif s1 == 5:
                    self.back()
            except Exception as e:
                raise e
                pass

    def work1(self):
        # 数据处理
        s = datax.Shuli()
        w = datax.WangqiLuyao()
        # 当原始数据更新后，须手动更新原始表格。平时不用。
        #s.execute_xlsx1('福彩3D', 'origin_data\福彩3D.xlsx', 'work_data\福彩3D_数理1.xlsx')
        #s.execute_xlsx2('福彩3D', 'work_data\福彩3D_数理1.xlsx', 'work_data\福彩3D_数理2.xlsx')
        #s.execute_xlsx1('体彩排列三', 'origin_data\体彩排列三.xlsx', 'work_data\体彩排列三_数理1.xlsx')
        #s.execute_xlsx2('体彩排列三', 'work_data\体彩排列三_数理1.xlsx', 'work_data\体彩排列三_数理2.xlsx')
        #w.execute_xlsx1('福彩3D', 'origin_data\福彩3D.xlsx', 'work_data\福彩3D_往期六爻1.xlsx')
        #w.execute_xlsx2('福彩3D', 'work_data\福彩3D_往期六爻1.xlsx', 'work_data\福彩3D_往期六爻2.xlsx')
        #w.execute_xlsx1('福彩七乐彩', 'origin_data\福彩七乐彩.xlsx', 'work_data\福彩七乐彩_往期六爻1.xlsx')
        #w.execute_xlsx2('福彩七乐彩', 'work_data\福彩七乐彩_往期六爻1.xlsx', 'work_data\福彩七乐彩_往期六爻2.xlsx')
        #w.execute_xlsx1('福彩双色球', 'origin_data\福彩双色球.xlsx', 'work_data\福彩双色球_往期六爻1.xlsx')
        #w.execute_xlsx2('福彩双色球', 'work_data\福彩双色球_往期六爻1.xlsx', 'work_data\福彩双色球_往期六爻2.xlsx')
        #w.execute_xlsx1('体彩大乐透', 'origin_data\体彩大乐透.xlsx', 'work_data\体彩大乐透_往期六爻1.xlsx')
        #w.execute_xlsx2('体彩大乐透', 'work_data\体彩大乐透_往期六爻1.xlsx', 'work_data\体彩大乐透_往期六爻2.xlsx')
        pass

    def work2(self):
        # 回归分析
        h = huiguifenxi.Huiguifenxi()
        h.ceshi()
        #analyse.analyse_1('福彩3D', 'work_data\福彩3D开奖_格式化2.xlsx', 'manual_data\福彩3D开奖_回归模型.xlsx', 'work_data\福彩3D开奖_概率分析.xlsx')
        #analyse.analyse_2('福彩3D', 'work_data\福彩3D开奖_概率分析.xlsx')
        pass

    def work3(self):
        # 可行性研究
        d = dulicecai.Dulicecai()
        # res = d.hezhiwuxingshahaofa(9,3,7)
        # print(res)
        # f = fenxi.Pailiexing()
        # f.lilungailv()
        k = kexingxingyanjiu.Gailvfenxi()
        k.zhixuan_gailv(path='work_data\福彩3D_数理2.xlsx')
        # k.zuxuan_gailv(path='work_data\福彩3D_数理2.xlsx')
        pass

    def work4(self):
        # 投注分析
        print('理论出组六概率：')
        print(P(10,3)/Pr(10,3))
        print('组六包7理论中奖概率：')
        print(C(4,3)*P(3,3)/Pr(10,3))
        print(Pr(10, 3, True))
        print('出现同号概率：')
        tongji_list = []
        for i in range(0, 365):
            rand1 = random.randint(0, 999)
            rand2 = random.randint(0, 999)
            print(Pr(10,3, li=True)[1][rand1])
            print(Pr(10, 3, li=True)[1][rand2])
            for j in range(0, 3):
                for k in range(0, 3):
                    if Pr(10,3, li=True)[1][rand1][j] == Pr(10,3, li=True)[1][rand2][k]:
                        if i not in tongji_list:
                            tongji_list.append(i)
                        print('同号：')
                        print(str(Pr(10,3, li=True)[1][rand1][j]) + '-' + str(Pr(10,3, li=True)[1][rand2][k]))
            print('=====================')
        print(len(tongji_list)/365)
        pass

    def work5(self):
        # 综合预测
        pass

    @staticmethod
    def back():
        os.system("cmd /k python ../test_cli.py")


if __name__ == '__main__':
    Cli()
