'''
此模块用来处理项目的绝对路径
'''
import os
#项目的根目录的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#数据
DATA_DIR = os.path.join(BASE_DIR, 'datas')
#配置文件
CONF_DIR = os.path.join(BASE_DIR, 'conf')
#log
LOG_DIR = os.path.join(BASE_DIR, 'logs')
#报告
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
#用例
TASTCASES_DIR = os.path.join(BASE_DIR, 'testcases')
