# Interface-Automation-Test
基于python requests + unittest 实现的接口自动化测试脚本  
技术栈：python 3.7 + requests + unittest  

依赖库：  
pip3 install requests==2.6.0  
pip3 install xlrd==1.1.0  
pip3 install XlsxWriter  
pip3 install pandas  

实现功能：  
1.在excel中编写测试用例，自动执行测试用例，自动生成测试报告；  
2.token(令牌)自动认证，开始输入账号和密码，将自动获取token，后续请求需要token的地方将自动填充；  
3.多excel支持。  

使用方式：  
1.将一个或n个测试用例文件放在cases目录下，测试用例扩展名为.xlsx;  
2.执行runner.py；  
3.自动执行测试；  
4.最后在report目录下生成 n+1 个测试报告。包括一个聚合报告和n个以cases目录下用例excel名为基础的分类报告。  

项目目录结构：  
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/2.PNG)  
用例填写说明：  
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/3.PNG)
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/5.PNG)  
报告说明：  
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/4.PNG)
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/6.PNG)
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/7.PNG)  
执行控制台输出：  
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/0.PNG)  
token（令牌）获取：
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/1.PNG)  
升级日志：  
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/2.0.1.PNG) 
项目目录结构：  
![image](https://raw.githubusercontent.com/yzqyfly/Interface-Automation-Test/master/img/list.png) 
