import pickle

"""
基础读文件函数readInfo(path)
函数名：readInfo(path)
输入：欲读取的文件名
输出：将读取到的数据以list的形式输出
"""
def readInfo(path):
    data = []
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = []
    return data


def writeInfo(kw, path):
    """
    将数据以字典的形式写入info.pickle文件
    """
    data = {"结果": kw["结果"],"接口名": kw["接口名"], "断言": kw["断言"], "用例": kw["用例"], "请求地址": kw["请求地址"], "请求体": kw["请求体"]
             , "响应码": kw["响应码"], "请求方式": kw["请求方式"], "响应体": kw['响应体']}
    _read = readInfo(path)
    result = []
    if _read:
        _read.append(data)
        result = _read
    else:
        result.append(data)
    with open(path, 'wb') as f:
        pickle.dump(result, f)
