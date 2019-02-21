# -*- coding: utf-8 -*-
import unittest
import requests
import time
import sys
import hashlib


#MD5加密函数,传入要加密的字符串，返回MD5加密后的字符串，32位
def md5_key(arg):
    md5 = hashlib.md5()#创建md5对象
    md5.update(arg.encode("utf8"))#生成加密串,必须指定要加密的字符串的字符编码
    return md5.hexdigest()#返回加密串


# 登录,获取token
def get_session():
    req = requests.session()
    #url = "https://cloudapi.usr.cn/usrCloud/user/login"  # 此处填写登录接口
    #data = {'account': 'rj09', 'password': '11da5e2caad4d291d16d60c62b0b43c6'}  # json格式输入用户名和密码。密码为MD5加密后
    url = input("请输入登录URL:")
    account = input("请输入账号:")
    password = input("请输入密码:")
    password = md5_key(password)
    time.sleep(1)
    print("正在请求令牌……")
    time.sleep(2)
    data = {'account': account, 'password': password}
    try:
        rps = req.post(url, json=data, verify=False)
        print("令牌获取成功:\n", rps.json()['data']['token'])
        print("3秒后执行测试")
        time.sleep(3)
        return rps.json()['data']['token']# 返回登录后的token
    except:
        print("异常中断,15秒后结束脚本")
        #time.sleep(15)
        #sys.exit(0)


class ParametrizedTestCase(unittest.TestCase):
    """ 需要参数化的测试用例类从此类继承
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)

    @classmethod
    def setUpClass(cls):
        cls.token = get_session() # 登录后的token
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @staticmethod
    def parametrize(testcase_klass, param=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite
