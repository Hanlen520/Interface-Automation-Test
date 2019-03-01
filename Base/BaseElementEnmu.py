import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Element(object):
    INFO_FILE = PATH("../Log/info.pickle") # 记录结果缓存
    API_FILES = PATH("../Cases/")  # 用例集
    REPORT_FILES = PATH("../Report/")#报告集