#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
install: python3 setup.py install
uninstall: pip3 uninstall [thispackname]
"""

from setuptools import setup, find_packages

setup(
    name="yxf_yixue_py",  # 安装后下划线自动变为-，包名称只用于安装卸载，程序中导入名称是实际代码文件夹名称。需手动保持一致
    version="0.1.0",
    author="yanyaming",
    packages=find_packages(where='.', include='*'),  # 需要指定这些参数才能正确搜索和安装，安装所有添加了__init__的目录
    include_package_data=True,  # 设置为True，通过MANIFEST.in包含其他类型文件
    install_requires=[
        "openpyxl",
    ],
    zip_safe=False,  # 非压缩安装，可见源代码
)
