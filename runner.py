import sys
sys.path.append("..")
import unittest
from TestCases.Api import ApiTest
from Base.BaseRunner import ParametrizedTestCase
from Base.BaseGetExcel import write_excel
from Base.BaseGetExcel import write_excels
from Base.BaseGetExcel import read_excels
from Base.BaseInit import BaseInit
from Base.BaseElementEnmu import Element

def runner_case():#运行测试初始化
    BaseInit().mk_file()#创建文件
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(ApiTest))
    unittest.TextTestRunner(verbosity=2).run(suite)#执行测试用例


if __name__ == '__main__':
    runner_case()#初始化
    tardataFilename = read_excels(Element.API_FILES)[1]#读取用例表，获取分类报告目标文件名
    write_excel(Element.INFO_FILE, Element.REPORT_FILE)#写入excel,聚合报告
    write_excels(Element.INFO_FILE, Element.REPORT_FILES, tardataFilename)#写入excel,分类报告
    print("执行完毕！")
    input("=====请查阅控制台执行日志=====")