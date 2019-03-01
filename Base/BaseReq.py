import requests
import json
import ast
from Base.BaseElementEnmu import Element
from Base.BaseStatistics import writeInfo
import urllib3
import datetime
urllib3.disable_warnings()#为了支持https协议

class Config(object):

    def __init__(self):
        pass

    app = {}#类全局变量

    '''
        添加token 函数
        函数名：settoken(dict,token)
        输入：字典,token
        输出：字典
        功能：传入的字典包含token键，则设置值为最新合法token
            若不包含token键，原样返回
    '''
    def settoken(self, dict, token):
        if dict.__contains__("token") == True:#dict.__contains__("键")函数：检查键是否在字典中
            dict["token"] = token  # 设token键值为最新的token
            return dict
        else:
            return dict

    '''
    生成URL函数
    传入协议，服务器地址，接口地址，拼接成请求的URL并返回
    '''
    def seturl(self,pr,ser,interface):
        return "%s://%s%s" % (pr,ser,interface)

    '''
    写入异常退出信息
    函数名：WritexceInfo
    输入：字典,异常内容
    输出：无
    '''
    def WritexceInfo(self, item, exceInfo):
        Config.app["接口名"] = item["接口名"]
        Config.app["用例"] = item["用例"]
        Config.app["请求体"] = str(item["请求体"])
        Config.app["请求地址"] = item["请求地址"]
        Config.app["断言"] = item.get("断言", "")
        Config.app["响应码"] = str("异常跳过")
        Config.app["响应体"] = str(exceInfo)
        Config.app["请求方式"] = item["请求方式"]
        Config.app["结果"] = str("异常跳过")
        writeInfo(Config.app, Element.INFO_FILE)  # 先写入data.pickle文件

    '''
    写入正确请求信息
    函数名：WritokInfo
    输入：字典,请求返回参，请求体字典，json格式化后的断言
    输出：无
    '''
    def WritokInfo(self, item, res, todict):
        Config.app["接口名"] = item["接口名"]
        Config.app["用例"] = item["用例"]
        Config.app["请求体"] = str(todict)
        Config.app["请求地址"] = item["请求地址"]
        Config.app["断言"] = item.get("断言", "")
        Config.app["响应码"] = str(res.status_code)
        Config.app["响应体"] = str(res.text)
        Config.app["请求方式"] = item["请求方式"]
        Config.app["结果"] = self.__check(Config.app["断言"], Config.app["响应体"])
        writeInfo(Config.app, Element.INFO_FILE)  # 先写入data.pickle文件

    '''
    写入报告分页信息
    函数名：WritNewRepInfo
    输入：无
    输出：无
    '''

    def WritNewRepInfo(self):
        Config.app["接口名"] = str("$$$$$")
        Config.app["用例"] = str("$$$$$")
        Config.app["请求体"] = str("$$$$$")
        Config.app["请求地址"] = str("$$$$$")
        Config.app["断言"] = str("$$$$$")
        Config.app["响应码"] = str("$$$$$")
        Config.app["响应体"] = str("$$$$$")
        Config.app["请求方式"] = str("$$$$$")
        Config.app["结果"] = str("$$$$$")
        writeInfo(Config.app, Element.INFO_FILE)  # 先写入data.pickle文件

    '''
    断言检查函数
    函数名：__check(self, hope, res)
    输入：断言，请求返回res
    输出：通过 or 失败
    '''

    def __check(self, hope, res):
        try:  # 没有发生异常证明是json格式的精准断言，也有可能是断言json格式错误。格式错误将按照模糊断言处理
            hope = json.loads(hope)
            fact = json.loads(res)
            for items in fact:
                if type(fact[items]) == list:
                    for item in fact[items]:
                        for k in hope:
                            if item.get(k, "") == hope[k]:
                                return "通过"
                if type(fact[items]) == dict:
                    for k in hope:
                        if fact[items].get(k, "") == hope[k]:
                            return "通过"
                for k in hope:
                    if fact.get(k, "") == hope[k]:
                        return "通过"
            return "失败"
        except:  # 发生异常执行模糊断言
            strres = str(res)
            strhope = str(hope)
            if strhope in strres:
                return "通过"
            else:
                return "失败"

    """
    英文化函数，删除制表符、换行符、空格，将中文引号、中括号、逗号替换为英文
    函数名：fom_Eng(self,zh_char)
    输入：含有中文字符的字符串
    输出：规范化后的字符串
    """
    def form_Eng(self, zh_char):
        return zh_char.replace('\r', '').replace('\n', '').replace('\t', '').replace('：', ':').replace('，', ',').replace('“', '"').replace('”', '"').replace('【', '[').replace('】', ']')
        #replace('欲替换的符号', '新符合')

    '''
    基础请求模块
    函数名：config_req(self, kw, token)
    输入：用例字典，token
    输出：无
    '''
    def config_req(self, kw, token):
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": token}

        for item in kw:
            if item["接口名"] == "$$$$$":#连续5个$，报告要分页，直接向数据文件中写入报告分页信息
                Config.WritNewRepInfo(self)
            else:
                url = Config().seturl(item["协议"], item["请求地址"], "")#拼接地址
                #print(item["请求体"])
                zh_char_body = Config.form_Eng(self, item["请求体"])#请求体消除中文符号
                zh_char_hope = Config.form_Eng(self, item["断言"])#断言消除中文符号
                #print(zh_char)

                try:#请求体json异常检测
                    todict_body = json.loads(zh_char_body)#请求体转换为json(字典)
                    jsondata = Config.settoken(self, todict_body, token) #给请求体添加token值
                except:#如果转换失败，将错误信息写入数据文件
                    Config.WritexceInfo(self,item, "请求体Json构造异常")
                    print("当前正在执行：", item["用例"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "警告:请求体Json构造异常")
                    continue
                """
                try:#断言json异常检测
                    json.loads(zh_char_hope)#断言转换为json(字典),此处不向后传参，只是帮助后面的断言函数（def __check(self, hope, res):）捕获异常，防止断言函数异常崩溃
                except:#如果转换失败，将错误信息写入数据文件
                    Config.WritexceInfo(self,item, "断言Json构造异常")
                    print("当前正在执行：", item["用例"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "警告:断言Json构造异常")
                    continue
                """

                if item["请求方式"] == "POST" or "post":
                    try:
                        res = requests.post(url, json=jsondata, headers=header, verify=False, timeout = 20) # 拼接完字典后发送请求,json形式。data形式的请求：res = requests.post(url, data=json.dumps(todict), headers=header, verify=False)
                    except:
                        Config.WritexceInfo(self, item, "Post请求异常")
                        print("当前正在执行：", item["用例"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "警告:Post请求异常")
                        continue
                elif item["请求方式"] == "GET" or "get":
                    try:
                        res = requests.get(url, json=jsondata, headers=header, verify=False, timeout=20)
                    except:
                        Config.WritexceInfo(self. item, "Get请求异常")
                        print("当前正在执行：", item["用例"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "警告:Get请求异常")
                        continue
                else:
                    Config.WritexceInfo(self, item, "请求方式异常")
                    print("当前正在执行：", item["用例"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "警告:请求方式异常")
                    pass

                Config.WritokInfo(self, item, res, jsondata)
                print("当前正在执行：", item["用例"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "执行成功")
