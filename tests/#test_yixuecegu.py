# build-in
import os  # 系统命令
import sys  # python设置
import shutil  # 高级文件操作
import timeit  # 计时相关
from datetime import datetime  # 日期时间
import time  # 时间相关

# init
sys.path.append(os.getcwd())  # 添加工程根目录(yixue_py3_yxf)到path环境变量

# module
import yixuecegu.datax as datax


class Cli:
    def __init__(self):
        print("===== 初始化工作目录 =====")
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))  # 基础路径为zhouyicecai目录
        print("基础路径：", BASE_DIR)
        os.chdir(BASE_DIR)  # 进入基础路径
        print("===== 开始工作 =====")
        try:  # 调用work()进入工作，直到工作完成
            time = timeit.timeit('work()', setup='from __main__ import work', number=1)
            print('===== 工作成功。 =====')
            print('消耗时间：{0}秒'.format(time))  # 计时
        except Exception as e:
            print('===== 工作失败。 =====')
            raise e
        finally:
            print("结束。")

    def work(self):
        while True:
            print('''
                #---------易学测股菜单----------#
                # 1.处理数据                    #
                # 2.训练预测模型                #
                # 3.预测股指升跌                #
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
            except Exception as e:
                raise e
                pass

    def work1(self):
        # 使原始数据变换为可用的卦爻数据。当原始数据更新后，须手动更新原始表格。平时不用。
        #datax.execute_xlsx1('上证指数', 'origin_data\上证指数.xlsx', 'work_data\上证指数_格式化1.xlsx')
        datax.execute_xlsx2('上证指数', 'work_data\上证指数_格式化1.xlsx', 'work_data\上证指数_格式化2.xlsx')
        #datax.execute_xlsx1('深证成指', 'origin_data\深证成指.xlsx', 'work_data\深证成指_格式化1.xlsx')
        #datax.execute_xlsx2('深证成指', 'work_data\深证成指_格式化1.xlsx', 'work_data\深证成指_格式化2.xlsx')
        #datax.execute_xlsx1('沪深300', 'origin_data\沪深300.xlsx', 'work_data\沪深300_格式化1.xlsx')
        #datax.execute_xlsx2('沪深300', 'work_data\沪深300_格式化1.xlsx', 'work_data\沪深300_格式化2.xlsx')

    def work2(self):
        pass

    def work3(self):
        pass


if __name__ == '__main__':
    Cli()
