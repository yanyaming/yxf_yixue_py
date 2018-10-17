# -*- coding: utf-8 -*-
import settings
import datetime
from utils.db import Db

"""
编程用到的技巧：内部类（对外隐藏）；类继承；构造函数重载；类变量

万年历特点：
1.起始于1900.1.31（1.31是阴历春节），阴历以春节（正月初一）为两年之交，不同于四柱
2.阳历和二十四节气是重要索引，四柱以立春为两年之交，是重点
3.此类只接收时间对象datetime，应当提前使用RealSolar类进行格式化
4.三种年的划分：阳历年（固定，无数术意义）、农历年（流转，无数术意义）、干支年（节气，重要）
5.三种月的划分：阳历月（固定，无数术意义）、农历月（月相，重要）、干支月（节气，包括月将星座，重要）
6.日、时统一
"""


# 所有历法均返回2元素列表，1是对象（若无则置空），2是字符串
class Calendar:
    def __init__(self):
        self.YEAR_START = 1900
        self.MONTH_START = 1
        self.DAY_START = 31
        self.YEAR_END = 2100
        self.db = Db()

    class Solar:
        # 太阳历，公历，公元纪年，例：公元 2012/12/21 19:00 星期一
        def __init__(self, datetime_str=None, return_list=True):
            self.out = Calendar()

        def solar(self, datetime_obj, jiyuan='公元'):
            # 基督纪元，公元
            # 黄帝纪元，开元，公元+2698
            # 佛祖纪元，佛历，公元+543
            solar_month = datetime_obj.month
            solar_day = datetime_obj.day
            solar_weekday_num, solar_weekday_name = self.__getWeekday(datetime_obj)
            solar_hour = datetime_obj.hour
            solar_minute = datetime_obj.minute
            if jiyuan == '公元':
                solar_year = datetime_obj.year
                return ['公元', solar_year, solar_month, solar_day, solar_hour, solar_minute, solar_weekday_num], '公元：' + str(solar_year) + '/' + str(solar_month) + '/' + str(solar_day) + ' ' + str(solar_hour) + ':' + str(solar_minute) + ' ' + str(solar_weekday_name)
            elif jiyuan == '开元':
                solar_year = datetime_obj.year + 2698
                return ['开元', solar_year, solar_month, solar_day, solar_hour, solar_minute, solar_weekday_num], '开元：' + str(solar_year) + '/' + str(solar_month) + '/' + str(solar_day) + ' ' + str(solar_hour) + ':' + str(solar_minute) + ' ' + str(solar_weekday_name)

        def __getWeekday(self, datetime_obj):
            solar_weekday_idx = datetime_obj.weekday()# weekday()的返回值从0-6依次为星期一到星期日
            querystr = self.out.db.select(tablename="[基础表-七曜]", column="[星期]",condition="where [程序编码序号]='{0}'".format(solar_weekday_idx))
            solar_weekday_name = str(querystr).strip('[]').strip('()').rstrip(',').strip('\'')
            return solar_weekday_idx + 1, solar_weekday_name

    class Lunar:
        # 太阴历，农历，例：2012年 正月 初一 子时 三刻
        # 一：月全黑规则 - 月全黑的日子是农历月的第一天。农历月周期由此而定。
        # 二：24节气规则 - 24节气把天文年按太阳角度分成24等份，15度一节气。 这个规则确定了农历和天文年的关系。
        # 三：冬至规则 - 冬至必须落在农历冬月。如果落不上，腊月之前就要添上一个月，成为闰年。
        # 四：闰月规则 - 如果是闰年，冬月后边第一个不含主节气的月份定为闰月。
        # 五：60年周期 - 农历年以60年为一周期。
        # 六：规则一和二的计算必须以中国南京紫金山天文台的观察为准。
        def __init__(self):
            self.out = Calendar()
            self.lunarYearInfo = self.out.db.get_tabledict_list("[基础表-阴历年分布表1900-2100]")
            self.lunarMonth = self.out.db.get_tabledict_list("[基础表-阴历月]")
            self.lunarDay = self.out.db.get_tabledict_list("[基础表-阴历日]")
            self.lunarKe = self.out.db.get_tabledict_list("[基础表-阴历刻]")
            self.dizhi = self.out.db.get_tabledict_list("[基础表-十二地支]")

        def lunar(self, datetime_obj):
            # 确定日期所在阳历年的阴历新年
            lunarYear_firstDay_str = self.lunarYearInfo[datetime_obj.year - self.out.YEAR_START]['阴历年起始阳历日'].lstrip('0d')
            lunarYear_firstDay = self.__datetimeStr2Obj(lunarYear_firstDay_str)

            # 年
            if datetime_obj < lunarYear_firstDay:  # 如果日期在新年之前，则找上一年
                lunar_year = datetime_obj.year - 1
                lunarYear_firstDay1_str = self.lunarYearInfo[datetime_obj.year - 1 - self.out.YEAR_START]['阴历年起始阳历日'].lstrip('0d')
                lunarYear_firstDay1 = self.__datetimeStr2Obj(lunarYear_firstDay1_str)
                lunar_day = (datetime_obj - lunarYear_firstDay1).days + 1
            else:
                lunar_year = datetime_obj.year
                lunar_day = (datetime_obj - lunarYear_firstDay).days + 1
            return_year = str(lunar_year) + '年'

            # 月，日，是否闰月
            lunar_month, lunar_monthday, isLeap = self.__getLunarMonth(lunar_year, lunar_day)
            lunar_leapMonth = int(self.lunarYearInfo[datetime_obj.year - self.out.YEAR_START]['闰月序号'])
            return_month = self.lunarMonth[lunar_month - 1]['汉字']
            if isLeap is True:
                return_month = '闰' + return_month
            return_monthday = self.lunarDay[lunar_monthday - 1]['汉字']
            if lunar_month >= lunar_leapMonth:  # 农历月数需加上闰月
                if (lunar_month == lunar_leapMonth) and (isLeap is False):
                    pass
                elif (lunar_month == lunar_leapMonth) and (isLeap is True):
                    lunar_month += 1
                elif lunar_leapMonth == 0:  # 闰月记录为0则表明此年无闰月
                    pass
                else:
                    lunar_month += 1

            # 时，刻
            lunar_hour = (datetime_obj.hour + 3) // 2
            if lunar_hour > 12:
                lunar_hour -= 12  # 23、0子1，1、2丑2，3、4寅3，21、22亥12
            if datetime_obj.hour in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 0]:
                lunar_ke = (datetime_obj.minute // 15) + 5
            else:
                lunar_ke = (datetime_obj.minute // 15) + 1  # 1-8
            return_hour = self.dizhi[lunar_hour - 1]['地支'] + '时'
            return_ke = self.lunarKe[lunar_ke - 1]['汉字']

            return ['农历', lunar_year, lunar_month, lunar_monthday, lunar_hour, lunar_ke, '闰' + str(lunar_leapMonth)],'农历：' + return_year + ' ' + return_month + ' ' + return_monthday + ' ' + return_hour + ' ' + return_ke

        def __getLunarMonth(self, lunar_year, lunar_day):
            # 输入：年，累计天数
            # 输出：最终落入的月，最终落入的月的天数，是否为闰月
            leapMonth = int(self.lunarYearInfo[lunar_year - self.out.YEAR_START]['闰月序号'])
            isLeap = False
            lunar_month = 0
            for m in range(1, 13):
                # 正常月份
                daysOfMonth = int(self.lunarYearInfo[lunar_year - self.out.YEAR_START][self.lunarMonth[m-1]['汉字']+'天数'])
                if lunar_day > daysOfMonth:
                    lunar_day -= daysOfMonth
                else:
                    lunar_month = m
                    break
                # 闰月
                if leapMonth == m:
                    daysOfMonth = int(self.lunarYearInfo[lunar_year - self.out.YEAR_START]['闰月天数'])
                    if lunar_day > daysOfMonth:
                        lunar_day -= daysOfMonth
                    else:
                        lunar_month = m
                        isLeap = True
                        break
            return lunar_month, lunar_day, isLeap

        @staticmethod
        def __datetimeStr2Obj(datetime_str):
            datetime_obj = datetime.datetime(
                # 编程语言问题：字符串切片截取——从0开始，从左界开始，顺数几个就截取几位
                # 例：2017-08-09
                int(datetime_str[0:4]),  # year=2017
                int(datetime_str[5:7]),  # month=08
                int(datetime_str[8:10]),  # day=09
            )
            return datetime_obj

    class SolarTerm:
        # 二十四节气，月将，星座，例：春分 第九天 大吉丑 白羊座
        def __init__(self):
            self.out = Calendar()
            self.solarTermInfo = self.out.db.select(tablename="[基础表-二十四节气年分布表1900-2100]", column="*")
            self.solarTermBase = self.out.db.get_tabledict_list("[基础表-二十四节气]")

        def solarTerm(self, datetime_obj):
            # 解析数据，获取对应此阳历年、上一阳历年的节气日期列表
            solarTermDays = self.solarTermInfo[datetime_obj.year - self.out.YEAR_START]
            solarTermDays_lastyear = self.solarTermInfo[datetime_obj.year - 1 - self.out.YEAR_START]
            # 给此阳历年、上一阳历年各节气建立日期时间对象
            solarTermDays_dt = []
            for i in range(0, 24):
                solarTermDays_dt.append(datetime.datetime(datetime_obj.year, (i + 2) // 2, int(solarTermDays[i+2])))
            solarTermDays_lastyear_dt = []
            for i in range(0, 24):
                solarTermDays_lastyear_dt.append(datetime.datetime(datetime_obj.year - 1, (i + 2) // 2, int(solarTermDays_lastyear[i+2])))
            # 判断输入日期的节气。得到：节气序号及名称，当前节气过了几日
            jieqiIdx = 0
            dayIdx = 0
            if datetime_obj < solarTermDays_dt[0]:  # 如果输入时间小于第一个节气，则节气为前一年冬至，需重新查询前一年的节气列表
                jieqiIdx = 23
                dayIdx = (datetime_obj - solarTermDays_lastyear_dt[jieqiIdx]).days + 1
            elif datetime_obj >= solarTermDays_dt[23]:  # 如果输入时间大于等于最后一个节气，则节气为当年冬至
                jieqiIdx = 23
                dayIdx = (datetime_obj - solarTermDays_dt[jieqiIdx]).days + 1
            else:  # 如果输入时间大于等于第一个节气且小于最后一个节气，先以第一个节气和第二个节气计算，如果输入时间介于两者之间则确认，否则继续判断
                for i in range(0, 23):
                    if solarTermDays_dt[i] <= datetime_obj < solarTermDays_dt[i + 1]:
                        jieqiIdx = i
                        dayIdx = (datetime_obj - solarTermDays_dt[jieqiIdx]).days + 1
            jieqi = self.solarTermBase[jieqiIdx]['节气名']
            # 求出月将和星座
            yuejiang = self.solarTermBase[jieqiIdx]['月将名称']+self.solarTermBase[jieqiIdx]['月将地支']
            xingzuo = self.solarTermBase[jieqiIdx]['西洋星座']
            return ['节气', jieqiIdx + 1, dayIdx], '节气：' + jieqi + ' 第' + str(dayIdx) + '天 ' + yuejiang + ' ' + xingzuo

        def solarTermJie(self, datetime_obj):
            # 求最近已往的节、交节后几天、下一节
            # 获取对应此年、上一年、下一年的节气日期列表
            solarTermDays = self.solarTermInfo[datetime_obj.year - self.out.YEAR_START]
            solarTermDays_f = self.solarTermInfo[datetime_obj.year - 1 - self.out.YEAR_START]
            solarTermDays_r = self.solarTermInfo[datetime_obj.year + 1 - self.out.YEAR_START]
            # 给此阳历年、上一年、下一年各节气建立日期时间对象
            dt_solarTerm = []
            for i in range(0, 24):
                dt_solarTerm.append(datetime.datetime(datetime_obj.year, (i + 2) // 2, int(solarTermDays[i+2]), 12))
            dt_solarTerm_f = []
            for i in range(0, 24):
                dt_solarTerm_f.append(datetime.datetime(datetime_obj.year - 1, (i + 2) // 2, int(solarTermDays_f[i+2]), 12))
            dt_solarTerm_r = []
            for i in range(0, 24):
                dt_solarTerm_r.append(datetime.datetime(datetime_obj.year + 1, (i + 2) // 2, int(solarTermDays_r[i+2]), 12))
            jieqiIdx = 0
            jieqiIdx_r = 0
            jieqiDay = None
            jieqiDay_r = None
            dayIdx = 0
            # 偶数序号为节
            if datetime_obj < dt_solarTerm[0]:  # 如果输入时间小于第一个节，则节为前一年大雪，需重新查询前一年的节气列表
                jieqiIdx = 22
                jieqiIdx_r = 0
                jieqiDay = dt_solarTerm_f[jieqiIdx]
                jieqiDay_r = dt_solarTerm[jieqiIdx_r]
                dayIdx = (datetime_obj - dt_solarTerm_f[jieqiIdx]).days + 1
            elif datetime_obj >= dt_solarTerm[22]:  # 如果输入时间大于等于最后一个节，则节气为当年大雪，下一节气需查询下一年
                jieqiIdx = 22
                jieqiIdx_r = 0
                jieqiDay = dt_solarTerm[jieqiIdx]
                jieqiDay_r = dt_solarTerm_r[jieqiIdx_r]
                dayIdx = (datetime_obj - dt_solarTerm[jieqiIdx]).days + 1
            else:  # 如果输入时间大于等于第一个节且小于最后一个节，先以第一个节和第二个节计算，如果输入时间介于两者之间则确认，否则继续判断
                for i in range(0, 22, 2):  # 步长2
                    if dt_solarTerm[i] <= datetime_obj < dt_solarTerm[i + 2]:
                        jieqiIdx = i
                        jieqiDay = dt_solarTerm[jieqiIdx]
                        if i == 22:
                            jieqiIdx_r = i - 22
                            jieqiDay_r = dt_solarTerm[jieqiIdx_r]
                        else:
                            jieqiIdx_r = i + 2
                            jieqiDay_r = dt_solarTerm[jieqiIdx_r]
                        dayIdx = (datetime_obj - dt_solarTerm[jieqiIdx]).days + 1
            jieqi = self.solarTermBase[jieqiIdx]['节气名']
            jieqi_r = self.solarTermBase[jieqiIdx_r]['节气名']
            return [jieqi, jieqiDay, dayIdx], [jieqi_r, jieqiDay_r]

        def solarTermDays(self, datetime_obj):
            solarTermDays = self.solarTermInfo[datetime_obj.year - self.out.YEAR_START]
            return solarTermDays[2:]

    class Ganzhilifa:
        def __init__(self):
            # 本应该全部放到数据库里去查，但懒得改了
            self.out = Calendar()
            # self.tiangan = self.out.db.get_tabledict("[基础表-十天干]")
            # self.dizhi = self.out.db.get_tabledict("[基础表-十二地支]")
            # self.bagua = self.out.db.get_tabledict("[基础表-八卦]")
            # self.liushisigua = self.out.db.get_tabledict("[基础表-六十四卦]")
            # self.liushijiazi = self.out.db.get_tabledict("[基础表-六十甲子]")
            # 天干表
            self.tianganName = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split(' ')
            # 地支表
            self.dizhiName = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')
            # 地支动物表
            self.dizhiDongwuName = '鼠 牛 虎 兔 龙 蛇 马 羊 猴 鸡 狗 猪'.split(' ')
            # 八卦表
            self.baguaName = '乾 兑 离 震 巽 坎 艮 坤'.split(' ')
            # 六十四卦表（易经卦序，上前下后）
            self.liushisiguaName = '乾为天 坤为地 水雷屯 山水蒙 水天需 天水讼 地水师 水地比 ' \
                                   '风天小畜 天泽履 地天泰 天地否 天火同人 火天大有 地山谦 雷地豫 ' \
                                   '泽雷随 山风蛊 地泽临 风地观 火雷噬嗑 山火贲 山地剥 地雷复 ' \
                                   '天雷无妄 山天大畜 山雷颐 泽风大过 坎为水 离为火 泽山咸 雷风恒 ' \
                                   '天山遁 雷天大壮 火地晋 地火明夷 风火家人 火泽睽 水山蹇 雷水解 ' \
                                   '山泽损 风雷益 泽天夬 天风姤 泽地萃 地风升 泽水困 水风井 ' \
                                   '泽火革 火风鼎 震为雷 艮为山 风山渐 雷泽归妹 雷火丰 火山旅 ' \
                                   '巽为风 兑为泽 风水涣 水泽节 风泽中孚 雷山小过 水火既济 火水未济'.split(' ')
            # 六十四卦爻位编码表（阳1阴0，上前下后）
            self.liushisiguaCode = [0b111111, 0b000000, 0b010001, 0b100010, 0b010111, 0b111010, 0b000010, 0b010000,
                                    0b110111, 0b111011, 0b000111, 0b111000, 0b111101, 0b101111, 0b000100, 0b001000,
                                    0b011001, 0b100110, 0b000011, 0b110000, 0b101001, 0b100101, 0b100000, 0b000001,
                                    0b111001, 0b100111, 0b100001, 0b011110, 0b010010, 0b101101, 0b011100, 0b001110,
                                    0b111100, 0b001111, 0b101000, 0b000101, 0b110101, 0b101011, 0b010100, 0b001010,
                                    0b100011, 0b110001, 0b011111, 0b111110, 0b011000, 0b000110, 0b011010, 0b010110,
                                    0b011101, 0b101110, 0b001001, 0b100100, 0b110100, 0b001011, 0b001101, 0b101100,
                                    0b110110, 0b011011, 0b110010, 0b010011, 0b110011, 0b001100, 0b010101, 0b101010]
            # 六十甲子表
            self.liushijiaziName = '甲子 乙丑 丙寅 丁卯 戊辰 己巳 庚午 辛未 壬申 癸酉 ' \
                                   '甲戌 乙亥 丙子 丁丑 戊寅 己卯 庚辰 辛巳 壬午 癸未 ' \
                                   '甲申 乙酉 丙戌 丁亥 戊子 己丑 庚寅 辛卯 壬辰 癸巳 ' \
                                   '甲午 乙未 丙申 丁酉 戊戌 己亥 庚子 辛丑 壬寅 癸卯 ' \
                                   '甲辰 乙巳 丙午 丁未 戊申 己酉 庚戌 辛亥 壬子 癸丑 ' \
                                   '甲寅 乙卯 丙辰 丁巳 戊午 己未 庚申 辛酉 壬戌 癸亥'.split(' ')

        # 规范化四柱干支，例：甲戌 壬申 癸酉 戊午 空亡：午未 午未 戌亥 子丑
        def ganzhi(self, datetime_obj, solarterm_str, wuzhu=False):
            solarTerm = solarterm_str[1].split('：')[1].split(' ')[0]
            nianzhu, nianzhu_kongwang = self.nianzhu(datetime_obj, solarTerm)
            yuezhu, yuezhu_kongwang = self.yuezhu(datetime_obj, nianzhu, solarTerm)
            rizhu, rizhu_kongwang = self.rizhu(datetime_obj)
            shizhu, shizhu_kongwang = self.shizhu(datetime_obj, rizhu)
            if wuzhu == '分柱':
                fenzhu = self.fenzhu(datetime_obj)
                return_str = '干支：' + nianzhu + ' ' + yuezhu + ' ' + rizhu + ' ' + shizhu + ' ' + fenzhu + '分柱'
            elif wuzhu == '刻柱':
                kezhu = self.kezhu(datetime_obj)
                return_str = '干支：' + nianzhu + ' ' + yuezhu + ' ' + rizhu + ' ' + shizhu + ' ' + kezhu + '刻柱'
            elif wuzhu == '月卦柱':
                yueguazhu = self.yueguazhu(datetime_obj)
                return_str = '干支：' + nianzhu + ' ' + yuezhu + ' ' + rizhu + ' ' + shizhu + ' ' + yueguazhu + '月卦柱'
            else:
                return_str = '干支：' + nianzhu + ' ' + yuezhu + ' ' + rizhu + ' ' + shizhu
            return return_str + ' 空亡（' + nianzhu_kongwang + ' ' + yuezhu_kongwang + ' ' + rizhu_kongwang + ' ' + shizhu_kongwang + '）'

        def nianzhu(self, datetime_obj, solarTerm):
            if (solarTerm in ['小寒', '大寒']) or (solarTerm == '冬至' and datetime_obj.month == 1):  # 阳历年首的两个半节气归为前一年
                ganzhi_year = datetime_obj.year - 1
            else:
                ganzhi_year = datetime_obj.year
            # 公历转换年干
            niangan_num = (ganzhi_year - 3) % 10  # 以4为尾数的年干为甲
            if niangan_num <= 0:
                niangan_num += 10
            niangan = self.tianganName[niangan_num - 1]
            # 公历转换年支
            nianzhi_num = (ganzhi_year - 3) % 12
            if nianzhi_num <= 0:
                nianzhi_num += 12
            nianzhi = self.dizhiName[nianzhi_num - 1]
            # 空亡
            nianzhu_kongwang = ''
            while niangan_num > 1:
                niangan_num -= 1
                nianzhi_num -= 1
                if nianzhi_num <= 2:
                    nianzhi_num += 12
            nianzhu_kongwang += self.dizhiName[nianzhi_num - 3]
            nianzhu_kongwang += self.dizhiName[nianzhi_num - 2]
            return niangan + nianzhi, nianzhu_kongwang

        def yuezhu(self, datetime_obj, nianzhu, solarTerm):
            # 月支固定，立春节交寅月
            # 1为寅月，2为卯月，，，11为子月，12为丑月
            querystr = self.out.db.select(tablename="[基础表-二十四节气]",column="[月建序号]",condition="where [节气名]='{0}'".format(solarTerm))[0]
            ganzhiMonth_index = int(str(querystr).strip('[]').strip('()').rstrip(',').strip('\''))
            # 月干按照歌诀
            # （年上起月）五虎遁：
            # 甲己丙为首，乙庚戊上头
            # 丙辛寻庚上，丁壬壬顺流
            # 戊癸何方发，甲寅好追求
            niangan = nianzhu[0:1]
            if niangan in ['甲', '己']:
                yuegan_index = 3  # 丙寅
            elif niangan in ['乙', '庚']:
                yuegan_index = 5  # 戊寅
            elif niangan in ['丙', '辛']:
                yuegan_index = 7  # 庚寅
            elif niangan in ['丁', '壬']:
                yuegan_index = 9  # 壬寅
            elif niangan in ['戊', '癸']:
                yuegan_index = 1  # 甲寅
            else:
                yuegan_index = 1
            # 转化
            ganzhiMonth_index += 2  # 新序号：寅3，，，亥12，子13，丑14
            yuegan_index = yuegan_index + ganzhiMonth_index - 3  # 干序配新月序：如甲年寅月3为丙干3，卯月4为丁干4；乙年寅月3为戊干5，卯月4为己干6
            if yuegan_index < 1:
                yuegan_index += 10
            if yuegan_index > 10:
                yuegan_index -= 10
            if ganzhiMonth_index > 12:
                ganzhiMonth_index -= 12  # 新序号：子1，丑2，寅3，，，亥12
            yuegan = self.tianganName[yuegan_index - 1]
            yuezhi = self.dizhiName[ganzhiMonth_index - 1]
            # 空亡
            yuezhu_kongwang = ''
            while yuegan_index > 1:
                yuegan_index -= 1
                ganzhiMonth_index -= 1
                if ganzhiMonth_index <= 2:
                    ganzhiMonth_index += 12
            yuezhu_kongwang += self.dizhiName[ganzhiMonth_index - 3]
            yuezhu_kongwang += self.dizhiName[ganzhiMonth_index - 2]
            return yuegan + yuezhi, yuezhu_kongwang

        def rizhu(self, datetime_obj):
            # 距离初始甲子日的偏移总日数，能被60整除者为甲子，计算余数
            # 1900/2/20 甲子，距离1/31有20日
            ganzhiDayIdx = (datetime_obj - datetime.datetime(Calendar().YEAR_START, Calendar().MONTH_START, Calendar().DAY_START)).days
            idx = (ganzhiDayIdx - 20) % 60
            rigan = self.tianganName[idx % 10]
            rizhi = self.dizhiName[idx % 12]
            rigan_index = idx % 10 + 1
            if rigan_index > 10:
                rigan_index -= 10
            rizhi_index = idx % 12 + 1
            if rizhi_index > 12:
                rizhi_index -= 12
            # 空亡
            rizhu_kongwang = ''
            while rigan_index > 1:
                rigan_index -= 1
                rizhi_index -= 1
                if rizhi_index <= 2:
                    rizhi_index += 12
            rizhu_kongwang += self.dizhiName[rizhi_index - 3]
            rizhu_kongwang += self.dizhiName[rizhi_index - 2]
            return rigan + rizhi, rizhu_kongwang

        def shizhu(self, datetime_obj, rizhu):
            # 时支固定，23点交子时
            ganzhiHour_index = (datetime_obj.hour + 3) // 2
            if ganzhiHour_index > 12:
                ganzhiHour_index -= 12  # 23、0子1，1、2丑2，3、4寅3，21、22亥12
            # 时干按照歌诀
            # （日上起时）五鼠遁：
            # 甲己还加甲，乙庚是丙初
            # 丙辛从戊起，丁壬居庚子
            # 戊癸在何方，壬子是真途
            rigan = rizhu[0:1]
            if rigan in ['甲', '己']:
                shigan_index = 1  # 甲子
            elif rigan in ['乙', '庚']:
                shigan_index = 3  # 丙子
            elif rigan in ['丙', '辛']:
                shigan_index = 5  # 戊子
            elif rigan in ['丁', '壬']:
                shigan_index = 7  # 庚子
            elif rigan in ['戊', '癸']:
                shigan_index = 9  # 壬子
            else:
                shigan_index = 1
            pass
            # 转化
            shigan_index = shigan_index + ganzhiHour_index - 1  # 干序配时序：如甲日子时1为甲干1；乙日子时1为丙干3，丑时2为丁干4
            if shigan_index < 1:
                shigan_index += 10
            if shigan_index > 10:
                shigan_index -= 10
            shigan = self.tianganName[shigan_index - 1]
            shizhi = self.dizhiName[ganzhiHour_index - 1]
            # 空亡
            shizhu_kongwang = ''
            while shigan_index > 1:
                shigan_index -= 1
                ganzhiHour_index -= 1
                if ganzhiHour_index <= 2:
                    ganzhiHour_index += 12
            shizhu_kongwang += self.dizhiName[ganzhiHour_index - 3]
            shizhu_kongwang += self.dizhiName[ganzhiHour_index - 2]
            return shigan + shizhi, shizhu_kongwang

        def fenzhu(self, dt):
            return ''

        def kezhu(self, dt):
            return ''

        def yueguazhu(self, dt):
            return ''

    class Fengshuilifa:
        def __init__(self):
            self.out = Calendar()
            self.solarTermInfo = self.out.db.select(tablename="[基础表-二十四节气年分布表1900-2100]", column="*")
            # 八卦表
            self.baguaName = '乾 兑 离 震 巽 坎 艮 坤'.split(' ')
            # 九星序号表
            self.jiuxingXName = '一白 二黑 三碧 四绿 五黄 六白 七赤 八白 九紫'.split(' ')
            # 九星名称表
            self.jiuxingMName = '贪狼 巨门 禄存 文曲 廉贞 武曲 破军 左辅 右弼'.split(' ')

        # 三元九运，四柱飞星，例：下元艮运 年九紫右弼 月一白贪狼 日二黑巨门 时一白贪狼
        def fengshui(self, datetime_obj, solarterm_str, ganzhi_str):
            # 准备节气信息
            solarTerm = solarterm_str[1].split('：')[1].split(' ')[0]
            # 准备农历信息（原程序需判断此农历年是否有闰月，有闰月则自闰月开始序号加1，影响月飞星计算）
            lunar_month_index = Calendar().Lunar().lunar(datetime_obj)[0][2] - 1
            # 准备干支四柱信息
            sizhu = ganzhi_str.split('：')[1].split(' ')
            nianzhu = sizhu[0]
            yuezhu = sizhu[1]
            rizhu = sizhu[2]
            shizhu = sizhu[3]
            # 计算
            yuanyun, ganzhi_year = self.yuanyun(datetime_obj, solarTerm)
            nianfeixing = self.nianfeixing(yuanyun, ganzhi_year)
            yuefeixing = self.yuefeixing(nianzhu, lunar_month_index)
            rifeixing, dt_solarTerm = self.rifeixing(datetime_obj)
            shifeixing = self.shifeixing(datetime_obj, rizhu, shizhu, dt_solarTerm)
            return '风水：' + yuanyun + ' 年' + nianfeixing + ' 月' + yuefeixing + ' 日' + rifeixing + ' 时' + shifeixing

        def yuanyun(self, datetime_obj, solarTerm):
            # 元运依干支年
            solar_month = datetime_obj.month
            if (solarTerm in ['小寒', '大寒']) or (solarTerm == '冬至' and solar_month == 1):  # 阳历年首的两个半节气归为前一个干支年
                ganzhi_year = datetime_obj.year - 1
            else:
                ganzhi_year = datetime_obj.year
            if 1864 <= ganzhi_year <= 1883:
                yuanyun = '上元坎运'
            elif 1884 <= ganzhi_year <= 1903:
                yuanyun = '上元坤运'
            elif 1904 <= ganzhi_year <= 1923:
                yuanyun = '上元震运'
            elif 1924 <= ganzhi_year <= 1943:
                yuanyun = '中元巽运'
            elif 1944 <= ganzhi_year <= 1963:
                yuanyun = '中元中运'
            elif 1964 <= ganzhi_year <= 1983:
                yuanyun = '中元乾运'
            elif 1984 <= ganzhi_year <= 2003:
                yuanyun = '下元兑运'
            elif 2004 <= ganzhi_year <= 2023:
                yuanyun = '下元艮运'
            elif 2024 <= ganzhi_year <= 2043:
                yuanyun = '下元离运'
            else:
                yuanyun = ''
            return yuanyun, ganzhi_year

        def nianfeixing(self, yuanyun, ganzhi_year):
            # 年飞星依干支年
            # 上元第一年为1（一白星入中宫）、第二年为9、第三年为8，以此类推。
            # 中元第一年为4（四绿星入中宫）、第二年为3、第三年为2，以此类推。
            # 下元第一年为7（七赤星入中宫）、第二年为6、第三年为5，以此类推。
            sanyuan = yuanyun[0:1]
            if sanyuan == '上':
                yearOffset = ganzhi_year - 1864
                jiuxingIdx = 1
            elif sanyuan == '中':
                yearOffset = ganzhi_year - 1924
                jiuxingIdx = 4
            elif sanyuan == '下':
                yearOffset = ganzhi_year - 1984
                jiuxingIdx = 7
            else:
                return ''
            while yearOffset > 0:
                jiuxingIdx -= 1
                if jiuxingIdx < 1:
                    jiuxingIdx += 9
                yearOffset -= 1
            feixing = self.jiuxingXName[jiuxingIdx - 1] + self.jiuxingMName[jiuxingIdx - 1]
            return feixing

        def yuefeixing(self, nianzhu, lunar_month_index):
            # 月飞星依农历月
            # 四孟年寅申巳亥年的正月为2（二黑星入中宫）、二月为1、三月为9，以此类推。
            # 四仲年子午卯酉年的正月为8（八白星入中宫）、二月为7、三月为6，以此类推。
            # 四季年辰戌丑未年的正月为5（五黄星入中宫）、二月为4、三月为3，以此类推。
            nianzhi = nianzhu[1:2]
            if nianzhi in ['寅', '申', '巳', '亥']:
                jiuxingIdx = 2
            elif nianzhi in ['子', '午', '卯', '酉']:
                jiuxingIdx = 8
            elif nianzhi in ['辰', '戌', '丑', '未']:
                jiuxingIdx = 5
            else:
                return ''
            jiuxingIdx -= lunar_month_index
            if jiuxingIdx < 1:
                jiuxingIdx += 9
            feixing = self.jiuxingXName[jiuxingIdx - 1] + self.jiuxingMName[jiuxingIdx - 1]
            return feixing

        def rifeixing(self, datetime_obj):
            # 日飞星依节气
            # （有争议，一说交气后起于甲子，一说交气后起于当日）此处用起于当日，与择吉黄历软件不同
            # 冬至，雨水、谷雨后自交气日起，分别自九宫飞星的一四七开始顺排，即：
            # 冬至当日为一白、第二日为二黑、第三日为三碧，以此类推。
            # 雨水当日为七赤、第二日为八白、第三日为九紫，以此类推。
            # 谷雨当日为四碧、第二日为五黄、第三日为六白，以此类推。
            # 夏至、处暑、霜降后自交气日起，分别自九宫飞星的九三六开始逆排，即：
            # 夏至当日为九紫、第二日为八白，第三日为七赤，以此类推。
            # 处暑当日为三碧、第二日为二黑，第三日为一白，以此类推。
            # 霜降当日为六白、第二日为五黄，第三日为四绿，以此类推。
            solarTermDays = self.solarTermInfo[datetime_obj.year - self.out.YEAR_START]
            dt_solarTerm = []
            for i in range(0, 24):
                dt_solarTerm.append(datetime.datetime(datetime_obj.year, (i + 2) // 2, int(solarTermDays[i+2])))
            solarTermDays1 = self.solarTermInfo[datetime_obj.year - 1 - self.out.YEAR_START]
            dt_solarTerm1 = datetime.datetime(datetime_obj.year - 1, 12, int(solarTermDays1[25]))
            if datetime_obj < dt_solarTerm[3]:  # 上一年冬至后
                dayIdx = (datetime_obj - dt_solarTerm1).days
                offset = 1
                shunxing = True
            elif dt_solarTerm[3] <= datetime_obj < dt_solarTerm[7]:  # 雨水后
                dayIdx = (datetime_obj - dt_solarTerm[3]).days
                offset = 7
                shunxing = True
            elif dt_solarTerm[7] <= datetime_obj < dt_solarTerm[11]:  # 谷雨后
                dayIdx = (datetime_obj - dt_solarTerm[7]).days
                offset = 4
                shunxing = True
            elif dt_solarTerm[11] <= datetime_obj < dt_solarTerm[15]:  # 夏至后
                dayIdx = (datetime_obj - dt_solarTerm[11]).days
                offset = 9
                shunxing = False
            elif dt_solarTerm[15] <= datetime_obj < dt_solarTerm[19]:  # 处暑后
                dayIdx = (datetime_obj - dt_solarTerm[15]).days
                offset = 3
                shunxing = False
            elif dt_solarTerm[19] <= datetime_obj < dt_solarTerm[23]:  # 霜降后
                dayIdx = (datetime_obj - dt_solarTerm[19]).days
                offset = 6
                shunxing = False
            elif datetime_obj >= dt_solarTerm[23]:  # 冬至后
                dayIdx = (datetime_obj - dt_solarTerm[23]).days
                offset = 1
                shunxing = True
            else:
                return ''
            if shunxing is True:
                jiuxingIdx = offset + dayIdx
                while jiuxingIdx > 9:
                    jiuxingIdx -= 9
            else:
                jiuxingIdx = offset - dayIdx
                while jiuxingIdx < 1:
                    jiuxingIdx += 9
            feixing = self.jiuxingXName[jiuxingIdx - 1] + self.jiuxingMName[jiuxingIdx - 1]
            return feixing, dt_solarTerm

        def shifeixing(self, datetime_obj, rizhu, shizhu, dt_solarTerm):
            # 时飞星依干支日和节气
            # 冬至后：
            # 寅申巳亥日，甲子时七赤，乙丑时八白，丙寅时九紫，以此类推。
            # 子午卯酉日，甲子时一白，乙丑时二黑，丙寅时三碧，以此类推。
            # 辰戌丑未日，甲子时四绿，乙丑时五黄，丙寅时六白，以此类推。
            # 夏至后：
            # 寅申巳亥日，甲子时起三碧，乙丑时二黑，丙寅时一白，以此类推。
            # 子午卯酉日，甲子时起九紫，乙丑时八白，丙寅时七赤，以此类推。
            # 辰戌丑未日，甲子时起六白，乙丑时五黄，丙寅时四绿，以此类推。
            rizhi = rizhu[1:2]
            if datetime_obj < dt_solarTerm[11] or datetime_obj >= dt_solarTerm[23]:  # 冬至后
                shunxing = True
                if rizhi in ['寅', '申', '巳', '亥']:
                    offset = 7
                elif rizhi in ['子', '午', '卯', '酉']:
                    offset = 1
                elif rizhi in ['辰', '戌', '丑', '未']:
                    offset = 4
                else:
                    return ''
            elif dt_solarTerm[11] <= datetime_obj < dt_solarTerm[23]:  # 夏至后
                shunxing = False
                if rizhi in ['寅', '申', '巳', '亥']:
                    offset = 3
                elif rizhi in ['子', '午', '卯', '酉']:
                    offset = 9
                elif rizhi in ['辰', '戌', '丑', '未']:
                    offset = 6
                else:
                    return ''
            else:
                return ''
            hourIdx = Calendar().Ganzhilifa().liushijiaziName.index(shizhu)
            if shunxing is True:
                jiuxingIdx = offset + hourIdx
                while jiuxingIdx > 9:
                    jiuxingIdx -= 9
            else:
                jiuxingIdx = offset - hourIdx
                while jiuxingIdx < 1:
                    jiuxingIdx += 9
            feixing = self.jiuxingXName[jiuxingIdx - 1] + self.jiuxingMName[jiuxingIdx - 1]
            return feixing

    class Zhongyilifa:
        def __init__(self):
            self.dizhiName = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')
            self.shierjingmaiName = '足少阳胆经 足厥阴肝经 手太阴肺经 手阳明大肠经 足阳明胃经 足太阴脾经 ' \
                                    '手少阴心经 手太阳小肠经 足太阳膀胱经 足少阴肾经 手厥阴心包经 手少阳三焦经'.split(' ')

        # 五运六气，司天在泉，子午流注。例：阳火运 少阴君火司天 少阳相火在泉 厥阴风木 手太阴肺经
        def zhongyi(self, solarterm_str, ganzhi_str):
            solarTerm = solarterm_str[1].split('：')[1].split(' ')[0]
            ganzhi = ganzhi_str.split('：')[1].split(' ')
            niangan = ganzhi[0][0:1]
            nianzhi = ganzhi[0][1:2]
            shizhi = ganzhi[3][1:2]
            wuyun = self.wuyun(niangan)
            sitian, zaiquan = self.sitianzaiquan(nianzhi)
            liuqi = self.liuqi(solarTerm)
            ziwuliuzhu = self.ziwuliuzhu(shizhi)
            return '中医：' + wuyun + ' ' + sitian + ' ' + zaiquan + ' ' + liuqi + ' ' + ziwuliuzhu

        def wuyun(self, niangan):
            wuyun = ''
            if niangan in ['甲', '丙', '戊', '庚', '壬']:
                wuyun += '阳'
            else:
                wuyun += '阴'
            if niangan in ['甲', '己']:
                wuyun += '土'
            if niangan in ['乙', '庚']:
                wuyun += '金'
            if niangan in ['丙', '辛']:
                wuyun += '水'
            if niangan in ['丁', '壬']:
                wuyun += '木'
            if niangan in ['戊', '癸']:
                wuyun += '火'
            wuyun += '运'
            return wuyun

        def sitianzaiquan(self, nianzhi):
            sitian = None
            zaiquan = None
            if nianzhi in '子 午'.split(' '):
                sitian = '少阴君火司天'
                zaiquan = '阳明燥金在泉'
            if nianzhi in '丑 未'.split(' '):
                sitian = '太阴湿土司天'
                zaiquan = '太阳寒水在泉'
            if nianzhi in '寅 申'.split(' '):
                sitian = '少阳相火司天'
                zaiquan = '厥阴风木在泉'
            if nianzhi in '卯 酉'.split(' '):
                sitian = '阳明燥金司天'
                zaiquan = '少阴君火在泉'
            if nianzhi in '辰 戌'.split(' '):
                sitian = '太阳寒水司天'
                zaiquan = '太阴湿土在泉'
            if nianzhi in '巳 亥'.split(' '):
                sitian = '厥阴风木司天'
                zaiquan = '少阳相火在泉'
            return sitian, zaiquan

        def liuqi(self, solarTerm):
            liuqi = None
            if solarTerm in ['大寒', '立春', '雨水', '惊蛰']:
                liuqi = '一阴厥阴风木'
            if solarTerm in ['春分', '清明', '谷雨', '立夏']:
                liuqi = '二阴少阴君火'
            if solarTerm in ['小满', '芒种', '夏至', '小暑']:
                liuqi = '一阳少阳相火'
            if solarTerm in ['大暑', '立秋', '处暑', '白露']:
                liuqi = '三阴太阴湿土'
            if solarTerm in ['秋分', '寒露', '霜降', '立冬']:
                liuqi = '二阳阳明燥金'
            if solarTerm in ['小雪', '大雪', '冬至', '小寒']:
                liuqi = '三阳太阳寒水'
            return liuqi

        def ziwuliuzhu(self, shizhi):
            ziwuliuzhu = self.shierjingmaiName[self.dizhiName.index(shizhi)]
            return ziwuliuzhu

    class Huangjilifa:
        # 皇极经世这里只通过软件固定代码查表的方式简单实现，除了一开始的节气，没有任何外部依赖
        def __init__(self):
            pass

        # 元会运世
        def huangjijingshi(self, datetime_obj, solarterm_str):
            solarTerm = solarterm_str[1].split('：')[1].split(' ')[0]
            if (solarTerm in ['小寒', '大寒']) or (solarTerm == '冬至' and datetime_obj.month == 1):  # 阳历年首的两个半节气归为前一年
                ganzhi_year = datetime_obj.year - 1
            else:
                ganzhi_year = datetime_obj.year
            yuan = self.yuan()
            hui = self.hui()
            yun = self.yun()
            shi = self.shi(ganzhi_year)
            xun = self.xun(ganzhi_year)
            nian = self.nian(ganzhi_year, shi)
            return '皇极：' + yuan + ' ' + hui + ' ' + yun + ' ' + shi + ' ' + xun + ' ' + nian

        def yuan(self):
            # 1元=12会=129600年
            # 1元4卦（离、乾、坎、坤），每卦统摄3会
            # 跨度太大，只要知道当前是坎卦午会
            yuan = '元（坎卦午会）'
            return yuan

        def hui(self):
            # 1会=30运=10800年
            # 1会统摄5正（会）卦
            # 午会（姤前2217-前57、大过前57-2103、鼎2103-4263、恒、巽）
            # 跨度太大，只要知道当前是午会、大过卦
            hui = '会（大过卦）'
            return hui

        def yun(self):
            # 1运=12世=360年
            # 每正（会）卦统摄6运卦（每运卦360年）：
            # 夬前57-303
            # 咸304-663
            # 困664-1023
            # 井1024-1383
            # 恒1384-1743
            # 姤1744-2103
            yun = '运（姤卦）'
            return yun

        def shi(self, ganzhi_year):
            # 1世=30年
            # 1运卦统摄6世卦，1世卦统摄2世60年
            # 乾1744—1803
            # 遁1804—1863
            # 讼1864—1923
            # 巽1924—1983
            # 鼎1984—2043
            # 大过2044—2103
            shi = None
            if 1864 <= ganzhi_year <= 1923:
                shi = '世（讼卦）'
            elif 1924 <= ganzhi_year <= 1983:
                shi = '世（巽卦）'
            elif 1984 <= ganzhi_year <= 2043:
                shi = '世（鼎卦）'
            elif 2044 <= ganzhi_year <= 2103:
                shi = '世（大过卦）'
            return shi

        def xun(self, ganzhi_year):
            # 1运卦变出6旬卦，每旬卦统摄10年
            # 计算有点麻烦，直接查表吧
            xun = None
            # 运卦：讼1864-1923
            if 1864 <= ganzhi_year <= 1923:
                if 1864 <= ganzhi_year <= 1873:
                    xun = '旬（履卦）'
                if 1874 <= ganzhi_year <= 1883:
                    xun = '旬（否卦）'
                if 1884 <= ganzhi_year <= 1893:
                    xun = '旬（姤卦）'
                if 1894 <= ganzhi_year <= 1903:
                    xun = '旬（涣卦）'
                if 1904 <= ganzhi_year <= 1913:
                    xun = '旬（未济卦）'
                if 1914 <= ganzhi_year <= 1923:
                    xun = '旬（困卦）'
            # 运卦：巽1924-1983
            if 1924 <= ganzhi_year <= 1983:
                if 1924 <= ganzhi_year <= 1933:
                    xun = '旬（小畜卦）'
                if 1934 <= ganzhi_year <= 1943:
                    xun = '旬（渐卦）'
                if 1944 <= ganzhi_year <= 1953:
                    xun = '旬（涣卦）'
                if 1954 <= ganzhi_year <= 1963:
                    xun = '旬（姤卦）'
                if 1964 <= ganzhi_year <= 1973:
                    xun = '旬（蛊卦）'
                if 1974 <= ganzhi_year <= 1983:
                    xun = '旬（井卦）'
            # 运卦：鼎1984-2043
            if 1984 <= ganzhi_year <= 2043:
                if 1984 <= ganzhi_year <= 1993:
                    xun = '旬（大有卦）'
                if 1994 <= ganzhi_year <= 2003:
                    xun = '旬（旅卦）'
                if 2004 <= ganzhi_year <= 2013:
                    xun = '旬（未济卦）'
                if 2014 <= ganzhi_year <= 2023:
                    xun = '旬（蛊卦）'
                if 2024 <= ganzhi_year <= 2033:
                    xun = '旬（姤卦）'
                if 2034 <= ganzhi_year <= 2043:
                    xun = '旬（恒卦）'
            # 运卦：大过2044-2103
            if 2044 <= ganzhi_year <= 2103:
                if 2044 <= ganzhi_year <= 2053:
                    xun = '旬（夬卦）'
                if 2054 <= ganzhi_year <= 2063:
                    xun = '旬（咸卦）'
                if 2064 <= ganzhi_year <= 2073:
                    xun = '旬（困卦）'
                if 2074 <= ganzhi_year <= 2083:
                    xun = '旬（井卦）'
                if 2084 <= ganzhi_year <= 2093:
                    xun = '旬（恒卦）'
                if 2094 <= ganzhi_year <= 2103:
                    xun = '旬（姤卦）'
            return xun

        def nian(self, ganzhi_year, shi):
            # 年卦以世卦起始，按照六十四卦圆图的顺序循环
            # 六十四卦圆图顺序
            yuantu = '复 颐 屯 益 震 ' \
                     '噬嗑 随 无妄 明夷 贲 ' \
                     '既济 家人 丰 革 同人 ' \
                     '临 损 节 中孚 归妹 ' \
                     '睽 兑 履 泰 大畜 ' \
                     '需 小畜 大壮 大有 夬 ' \
                     '姤 大过 鼎 恒 巽 ' \
                     '井 蛊 升 讼 困 ' \
                     '未济 解 涣 蒙 师 ' \
                     '遁 咸 旅 小过 渐 ' \
                     '蹇 艮 谦 否 萃 ' \
                     '晋 豫 观 比 剥'.split(' ')
            offset = 0
            idx = 0
            if shi == '世（讼卦）':
                idx = ganzhi_year - 1864
                offset = yuantu.index('讼')
            elif shi == '世（巽卦）':
                idx = ganzhi_year - 1924
                offset = yuantu.index('巽')
            elif shi == '世（鼎卦）':
                idx = ganzhi_year - 1984
                offset = yuantu.index('鼎')
            elif shi == '世（大过卦）':
                idx = ganzhi_year - 2044
                offset = yuantu.index('大过')
            if offset + idx >= 60:
                res = yuantu[offset + idx - 60]
            else:
                res = yuantu[offset + idx]
            nian = '年（' + res + '卦）'
            return nian
