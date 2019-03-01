import xlrd
import xlsxwriter
from Base.BaseElementEnmu import Element
from Base.BaseExcel import *
from Base.BaseStatistics import readInfo
import pandas
import os
import time

"""
        函数名:read_excels_data(inputdir = '../Cases/')
        功能:读取某目录下的多个excel文件内容
        输入:excel集合目录
        输出:列表:excel中的每一行
    [
        [
    {
        '接口名':'aaa',
        '用例':'用例aaa',
            ……,
        '请求参数':'balabalabala'
    },
    {
        '接口名':'bbb',
        '用例':'用例bbb',
            ……,
        '请求参数':'balabalabala'
    }
]
"""
def read_excels_data(inputdir):
    dataframe = pandas.DataFrame(columns=['接口名','用例','请求地址','请求体','断言','协议','请求方式'])
    for parents, dirnames, filenames in os.walk(inputdir):#遍历用例目录下的所有excel文件
        for filename in filenames:#依次读取每个文件
            try:
                datafile = pandas.read_excel(os.path.join(parents, filename))#单个excel里面的数据给datafile
                #print("当前正在处理：%s" % filename)  # 打印每一个excel的文件名
                dataframe = dataframe.append(datafile, ignore_index=True)  # 多个datafile数据按照属性列追加到dataframe
            except:
                print("Warning:多excel打开异常，请检查文件格式并确认文件处于关闭状态！")
                continue
    Tolist = dataframe.to_dict(orient="records")#按数据列属性为所索引，数据行为值，转换为列表
    return Tolist

"""
功能：读取目标目录下excel文件名
函数名：read_excels_names(filepath)
输入：文件目录
返回：excel文件名列表
"""
def read_excels_names(filepath):
    filenamelist = []
    for parents, dirnames, filenames in os.walk(filepath):
        return filenames

"""
    写excel，数据源为传入的列表数据，写入到目标数据文件(.xlsx)
    函数名：write_excel_excelres(resdata, tardata)
    输入：源数据列表，目标数据文件路径
    输出：无输出。数据写入到目标数据文件
"""
def write_excel(resdata, tardata):
    workbook = xlsxwriter.Workbook(tardata)#打开一个excel文件，给workbook
    operateReport = OperateReport(workbook)#实例化OperateReport

    worksheet1 = workbook.add_worksheet("测试概况")#sheet1汇总测试数据
    operateReport.WriteFun_to_Excel(worksheet1)#计算统计数据
    operateReport.pie(workbook, worksheet1)

    worksheet2 = workbook.add_worksheet("测试详情")#在打开的excel中新建一个工作簿(sheet)worksheet1
    operateReport.detail(worksheet2, resdata)#在数据文件中读取数据写入到构造的单元格中

    operateReport.close()#关闭excel

"""
    功能：生成报告，在源数据文件(.pickle)中取数据，生成一个聚合报告和若干分类报告
    函数名：buit_report()
    输入：无
    输出：无输出。构造报告完成
"""
def buit_report():
    data = readInfo(Element.INFO_FILE)
    SUMreportPath = Element.REPORT_FILES + "\\" + "0_聚合报告.xlsx"#生成聚合报告文件位置
    print("正在生成聚合报告：",SUMreportPath)
    write_excel(data, SUMreportPath)#生成聚合报告
    time.sleep(2)  # 等待IO
    pagenum = 0
    templist = []
    j = 0
    names = read_excels_names(Element.API_FILES)#获取用例excel文件名
    #以下遍历数据源，统计报告需要分多少页
    for item in data:
        if item["结果"] == "$$$$$":
            pagenum += 1

    #重新从聚合报告.xlsx里面取出数据来拆分出分类报告
    data = pandas.read_excel(SUMreportPath, sheet_name="测试详情",header=1)  # 打开聚合报告.xlsx的测试详情工作簿,从第二行开始取数据，前两行是表头，无意义
    # rows = data.shape[0]#获取行数。shape[1]获取列数
    Tolist = data.to_dict(orient="records")  # 按数据列属性为所索引，数据行为值，转换为列表


    if pagenum == len(names): #如果用例excel文件数和分页符数一样，则按照用例excel文件名生成分类报告
        for i in range(len(Tolist)):
            if Tolist[i]["结果"] == "$$$$$":
                SUBreportPath = Element.REPORT_FILES + "\\" + str(j + 1) + "_分类报告_" + names[j]  # 根据测试用例文件名生成报告路径和文件名
                # print("当前即将写入分类报告中的数据：", templist)
                print("正在生成分类报告：", SUBreportPath)
                write_excel(templist, SUBreportPath)  # 写入分类报告excel
                time.sleep(2)  # 等待IO
                templist = []  # 清空列表
                j += 1
            else:
                templist.append(Tolist[i])  # 遇不到分页符，就把当前元素加入到一个临时列表
    else: #如果用例excel文件数和分页符数不一样，则按1234……自然顺序生成分类报告的文件名
        for i in range(len(Tolist)):
            if Tolist[i]["结果"] == "$$$$$":
                SUBreportPath = Element.REPORT_FILES + "\\" + str(j + 1) + "_分类报告第" + str(j + 1) + "页.xlsx"  # 根据测试用例文件名生成报告路径和文件名
                print("正在生成分类报告：", SUBreportPath)
                write_excel(templist, SUBreportPath)  # 写入分类报告excel
                time.sleep(2)  # 等待IO
                templist = []  # 清空列表
                j += 1
            else:
                templist.append(Tolist[i])  # 遇不到分页符，就把当前元素加入到一个临时列表


if __name__ == "__main__":
    #ls = read_excel(Element.API_FILE)
    #print(ls)
    #datas = read_excels(Element.API_FILES)
    #write_excels(Element.INFO_FILE, Element.REPORT_FILES, datas[1])
    #print(datas)
    #print(readInfo(Element.INFO_FILE))
    buit_report()
    #print(read_excels_names(Element.API_FILES))
    pass
