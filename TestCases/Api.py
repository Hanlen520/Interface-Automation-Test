from Base.BaseRunner import ParametrizedTestCase
#from Base.BaseGetExcel import read_excel
from Base.BaseGetExcel import read_excels
from Base.BaseReq import Config
from Base.BaseElementEnmu import Element
from Base.BaseIni import BaseIni

class ApiTest(ParametrizedTestCase):
    def test_api(self):
        ls = read_excels(Element.API_FILES)[0]#读取用例excel，得到一个列表
        token = self.token#得到token
        Config().config_req(ls, token)#将包含用例的列表和token传入请求模块config_req

    @classmethod
    def setUpClass(cls):
        super(ApiTest, cls).setUpClass()
        cls.token
