import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Element(object):
    INFO_FILE = PATH("../Log/info.pickle") # 记录结果缓存
    REPORT_FILE = PATH("../Report/0_聚合报告.xlsx") # 测试报告
    REPORT_FILES = PATH("../Report/")#报告集，多excel文件
    API_FILE = PATH("../Cases/api.xlsx") # 用例文件
    API_FILES = PATH("../Cases/")#用例集，多excel