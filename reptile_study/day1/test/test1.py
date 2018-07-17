
# 爬虫需要的第三方工具，安装及其使用
from urllib import robotparser

import builtwith

a = builtwith.parse('http://www.baidu.com/')
# 网站使用框架
# print(a)


import ssl

# ssl._create_default_https_context = ssl._create_unverified_context
# # 不验证证书
# b = builtwith.parse('https://www.jianshu.com/')
#
# print( b)
#
import whois

c = whois.whois('ppddog.cn')
# 查看网站所有者
# print(c)


# 查看是否允许被爬虫抓取。
parser = robotparser.RobotFileParser()
d = parser.can_fetch('Baiduspider', 'www.baidu.com')


print(d)
