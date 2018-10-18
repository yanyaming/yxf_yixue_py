yxf_yixue_py : 易学软件
=========================================================

1.历法（万年历）  
2.各数术模块（已完成：八字、六爻、小成图、金口诀，未来可添加：紫微斗数、风水、吠陀占星）  
3.预测应用（探索性代码，暂时无用）  


环境依赖（此项目非常依赖中文和统一编码，2版本对中文非常不友好，必须使用3版本）
--------

python==3.6  
openpyxl  

python3解决方案：  
安装python3（已整理安装脚本）  
在项目的所有代码开头加上这句：#!/usr/bin/python3（有了这句，编码声明就可以删掉）  


待解决
------

自动分析代码——内容太多，时间太少  
预测的理论性理解——超出物质科学范围，悟  
预测实战的可靠性——缺少大批量实验；占卜术预测准确性受心理状态影响忽高忽低，时而不准时而神准，很难可靠预测；命理术较为客观容易实现  
数字预测  


代码结构
--------

    /utils——通用代码
    /wannianli——万年历（农历与节气无法逻辑推算，需要数据库，目前只得到200年数据）
    /bazi——八字
    /jinkoujue——金口诀
    /liuyao——六爻
    /xiaochengtu——小成图
    /#ziweidoushu——（紫微斗数，希望未来能够加入）
    /#feituozhanxing——（吠陀占星，希望未来能够加入）
	/#app_yixuececai——（易学测彩的初步探索，暂时无用）
	/#app_yixuecegu——（易学测股的初步探索，暂时无用）
