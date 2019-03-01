import os
import datetime

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class OperateReport:

    def __init__(self, wd):
        self.wd = wd

    """
    生成饼图函数
    函数名：pie(workbook, worksheet)
    输入：工作表，工作簿
    输出：
    """
    def pie(self, workbook, worksheet):
        chart1 = workbook.add_chart({'type': 'pie'})
        chart1.add_series({'name': '比例图', #标题
                           'categories': '=测试概况!$E$7:$E$9', #图例
                           'values': '=测试概况!$F$7:$F$9'})#数据
        chart1.set_title({'name': '执行统计'})
        chart1.set_style(10)
        worksheet.insert_chart('B3', chart1, {'x_offset': 25, 'y_offset': 10})

    """
    向工作簿(sheet1-测试概况)写入数据的函数
    函数名：WriteFun_to_Excel(self, worksheet)
    输入：需要写入函数的工作簿
    输出：无
    """

    def WriteFun_to_Excel(self, worksheet):
        # 设置列宽
        worksheet.set_column("A:A", 25)  # 结果列
        worksheet.set_column("B:B", 25)  # 接口名列
        worksheet.set_column("C:C", 25)  # 用例列
        worksheet.set_column("D:D", 25)  # 请求体列
        worksheet.set_column("E:E", 25)  # 请求地址列
        worksheet.set_column("F:F", 25)  # 断言列
        worksheet.set_column("G:G", 25)  # 响应码列
        worksheet.set_column("H:H", 25)  # 响应体列
        # 表头USR-API-Test-测试概况
        worksheet.merge_range('A1:H1', 'USR-API-Test-测试概况', get_format(self.wd, {'bold': True, 'font_size': 18,'align': 'center', 'valign': 'vcenter', 'bg_color': 'blue', 'font_color': '#ffffff'}))


        # write(单元格，数据或字符串，格式（单元格，背景色，前景色）)，行列从0开始
        worksheet.write("E7", "通过数", colo_format(self.wd, "7CFC00", "black"))#绿底黑字
        worksheet.write("E8", "失败数", colo_format(self.wd, "red", "black"))#红底黑字
        worksheet.write("E9", "异常跳过数", colo_format(self.wd, "#EEEE00", "black"))#黄底黑字
        worksheet.write("E10", "用例总计", colo_format(self.wd, "#ffffff", "black"))#白底黑字
        worksheet.write("E11", "通过率", colo_format(self.wd, "#ffffff", "black"))#白底黑字
        worksheet.write("E12", "报告日期", colo_format(self.wd, "#ffffff", "black"))  # 白底黑字


        worksheet.write("F7", '=COUNTIF(测试详情!A3:A256,"通过")')#姑且统计到256行，主要是目前水平还达不到知道具体行数
        worksheet.write("F8", '=COUNTIF(测试详情!A3:A256,"失败")')
        worksheet.write("F9", '=COUNTIF(测试详情!A3:A256,"异常跳过")')
        worksheet.write("F10", '=SUM(F7:F9)')
        worksheet.write("F11", '=TEXT(F7/(F10-F9),"0%")')
        worksheet.write("F12", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    """
        向工作簿(sheet2-测试详情)写入数据的函数
        函数名：detail(self, worksheet, info)
        输入：工作簿实例，将要写入到工作簿的数据列表
        输出：无
    """
    def detail(self, worksheet, info):
        # 设置列宽
        worksheet.set_column("A:A", 10)#结果列
        worksheet.set_column("B:B", 20)#接口名列
        worksheet.set_column("C:C", 30)#用例列
        worksheet.set_column("D:D", 40)#请求体列
        worksheet.set_column("E:E", 20)#请求地址列
        worksheet.set_column("F:F", 20)#断言列
        worksheet.set_column("G:G", 10)#响应码列
        worksheet.set_column("H:H", 40)#响应体列

        #设置行高
        worksheet.set_row(1, 30)

        #表头USR-API-Test-测试详情
        worksheet.merge_range('A1:H1', 'USR-API-Test-测试详情', get_format(self.wd, {'bold': True, 'font_size': 18, 'align': 'center', 'valign': 'vcenter', 'bg_color': 'blue','font_color': '#ffffff'}))

        #标题
        _write_center(worksheet, "A2", '结果', self.wd)
        _write_center(worksheet, "B2", '接口名', self.wd)
        _write_center(worksheet, "C2", '用例', self.wd)
        _write_center(worksheet, "D2", '请求体', self.wd)
        _write_center(worksheet, "E2", '请求地址', self.wd)
        _write_center(worksheet, "F2", '断言', self.wd)
        _write_center(worksheet, "G2", '响应码', self.wd)
        _write_center(worksheet, "H2", '响应体', self.wd)

        #从第三行开始写入实际测试结果数据
        temp = 3

        for item in info:
            if item["结果"] == "失败":
                _write_center_Red(worksheet, "A" + str(temp), item["结果"], self.wd)#如果用例失败，标记为红色
            else:
                _write_center(worksheet, "A" + str(temp), item["结果"], self.wd)
            _write_center(worksheet, "B" + str(temp), item["接口名"], self.wd)
            _write_center(worksheet, "C" + str(temp), item["用例"], self.wd)
            _write_center(worksheet, "D" + str(temp), item["请求体"], self.wd)
            _write_center(worksheet, "E" + str(temp), item["请求地址"], self.wd)
            _write_center(worksheet, "F" + str(temp), item["断言"], self.wd)
            _write_center(worksheet, "G" + str(temp), item["响应码"], self.wd)
            _write_center(worksheet, "H" + str(temp), item["响应体"], self.wd)
            temp += 1

    def close(self):
        self.wd.close()



    """
        格式类函数
    """

def colo_format(wd,bgcol,foncol):#报告中的彩色显示,单元格，背景色，前景色
    return wd.add_format({'bg_color': bgcol, 'align': 'center', 'font_color': foncol, 'bold': 1, 'underline': 1, 'font_size': 12})

def get_format(wd, option={}):
    return wd.add_format(option)

def fail_format(wd):#失败用例红色高亮显示,红底黑字
    return wd.add_format({'bg_color': 'red', 'align': 'center', 'font_color': 'black', 'bold': 1, 'underline': 1, 'font_size': 12})

def get_format_center(wd, num=0):#num=1每一行会有宽度为1px的黑色分割线
    return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})

def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)

def _write_center(worksheet, cl, data, wd):#_write_center(工作簿, 单元格位置, 数据, 样式)
    return worksheet.write(cl, data, get_format_center(wd))

def _write_center_Red(worksheet, cl, data, wd):#_write_center(工作簿, 单元格位置, 数据, 样式)
    return worksheet.write(cl, data, fail_format(wd))

def set_row(worksheet, num, height):
    worksheet.set_row(num, height)

if __name__ == '__main__':
    pass
