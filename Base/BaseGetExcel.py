import xlrd
import xlsxwriter
from Base.BaseElementEnmu import Element
from Base.BaseExcel import *
from Base.BaseStatistics import readInfo
import pandas
import os

''''
读单个excel中的测试用例，返回一个列表，列表里面是以表格列名为键，每一行数据为值的字典集，每一行数据存在一个字典。
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
'''
def read_excel(file='c:/test.xls'):
    data = xlrd.open_workbook(file)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(0)  # one rows data
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                # row[i] = colnames[i] + row[i]
                app[colnames[i]] = row[i]
            list.append(app)#新读出的字典数据追加到list
    return list

"""
        函数名:read_excels(inputdir = '../Cases/')
        功能:读取多个excel文件
        输入:excel集合目录
        输出:列表[0]:excel中的每一行
             列表[1]:每个excel的文件名
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
],
[
"excel1文件名",
"excel2文件名",
"excel3文件名"
]
"""
def read_excels(inputdir = '../Cases/'):
    dataframe = pandas.DataFrame(columns=['接口名','用例','请求地址','请求体','断言','协议','请求方式'])
    filenamelist = []
    for parents, dirnames, filenames in os.walk(inputdir):#遍历用例目录下的所有excel文件
        for filename in filenames:#依次读取每个文件
            try:
                datafile = pandas.read_excel(os.path.join(parents, filename))#单个excel里面的数据给datafile
                #print("当前正在处理：%s" % filename)  # 打印每一个excel的文件名
            except:
                print("Warning:多excel打开异常，请检查文件格式并确认文件处于关闭状态！")
                continue
            filenamelist.append(filename)#excel文件名加入filenamelist
            dataframe = dataframe.append(datafile, ignore_index=True)#多个datafile数据按照属性列追加到dataframe
    Tolist = dataframe.to_dict(orient="records")#按数据列属性为所索引，数据行为值，转换为列表
    return Tolist, filenamelist

"""
    写单个excel，在源数据文件(.pickle)中取数据，写入到目标数据文件(.xlsx)
    函数名：write_excel(resdata, tardata)
    输入：源数据文件，目标数据文件
    输出：无输出。数据写入到目标数据文件
"""
def write_excel(resdata, tardata):
    workbook = xlsxwriter.Workbook(tardata)#打开一个excel文件，给workbook
    operateReport = OperateReport(workbook)#实例化OperateReport

    worksheet1 = workbook.add_worksheet("测试概况")#sheet1汇总测试数据
    operateReport.WriteFun_to_Excel(worksheet1)#计算统计数据
    operateReport.pie(workbook, worksheet1)

    worksheet2 = workbook.add_worksheet("测试详情")#在打开的excel中新建一个工作簿(sheet)worksheet1
    operateReport.detail(worksheet2, readInfo(resdata))#在数据文件中读取数据写入到构造的单元格中

    operateReport.close()#关闭excel

"""
    写单个excel，数据源为传入的列表数据，写入到目标数据文件(.xlsx)
    函数名：write_excel_excelres(resdata, tardata)
    输入：源数据文件，目标数据文件
    输出：无输出。数据写入到目标数据文件
"""
def write_excel_excelres(resdata, tardata):
    workbook = xlsxwriter.Workbook(tardata)#打开一个excel文件，给workbook
    operateReport = OperateReport(workbook)#实例化OperateReport

    worksheet1 = workbook.add_worksheet("测试概况")#sheet1汇总测试数据
    operateReport.WriteFun_to_Excel(worksheet1)#计算统计数据
    operateReport.pie(workbook, worksheet1)

    worksheet2 = workbook.add_worksheet("测试详情")#在打开的excel中新建一个工作簿(sheet)worksheet1
    operateReport.detail(worksheet2, resdata)#在数据文件中读取数据写入到构造的单元格中

    operateReport.close()#关闭excel


"""
    写多个excel，在源数据文件(.pickle)中取数据，写入到目标数据文件(.xlsx)
    函数名：write_excels(resdata, tardataFile, tardataFilename)
    输入：源数据文件，目标数据文件夹，目标数据文件名列表
    输出：无输出。数据写入到目标数据文件
"""
def write_excels(resdata, tardataFile, tardataFilename):
    data = pandas.read_excel(Element.REPORT_FILE, sheet_name="测试详情", header=1)#打开聚合报告.xlsx的测试详情工作簿,从第二行开始取数据，前两行是表头，无意义
    #rows = data.shape[0]#获取行数。shape[1]获取列数
    Tolist = data.to_dict(orient="records")  # 按数据列属性为所索引，数据行为值，转换为列表
    #print(Tolist[0]["结果"])
    templist = []
    j = 0
    for i in range(len(Tolist)):
        if Tolist[i]["结果"] == "$$$$$":
            realnamepath = tardataFile + "\\" + str(j+1) + "_分类报告_" + tardataFilename[j]  # 根据测试用例文件名生成报告路径和文件名
            print("当前文件名：", realnamepath)
            #print("遇到了分页符")
            #print("当前即将写入分类报告中的数据：", templist)
            print("正在生成分类报告：", realnamepath)
            write_excel_excelres(templist, realnamepath)#写入分类报告excel
            time.sleep(5)#等待IO，数据量较大时偶尔存在数据还没有写完，缓存列表就被清空的情况
            templist = []#清空列表
            j += 1
        else:
            templist.append(Tolist[i])#遇不到分页符，就把当前元素加入到一个临时列表


if __name__ == "__main__":
    #ls = read_excel(Element.API_FILE)
    #print(ls)
    #datas = read_excels(Element.API_FILES)
    #write_excels(Element.INFO_FILE, Element.REPORT_FILES, datas[1])
    #print(datas)
    #print(readInfo(Element.INFO_FILE))
    pass