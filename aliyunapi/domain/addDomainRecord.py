from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
import sys
from aliyunapi.tool.Utils import *


argcheck(sys.argv, 4)
sys.argv.pop(0)
"""
命令行运行需要4个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 主机记录， 记录类型，记录值。调用只在在zjrongxiang.com的域上进行添加二级域名
"""
account, rr, recordtype, value = sys.argv
print(account, rr, recordtype, value)

region, akid, aksrt = akconfig(account)
# print(region, akid, aksrt)
client = AcsClient(akid, aksrt, region)
request = AddDomainRecordRequest()
request.set_accept_format('json')

request.set_DomainName("zjrongxiang.com")
request.set_RR(rr)
request.set_Type(recordtype)
request.set_Value(value)

response = client.do_action_with_exception(request)
print(str(response, encoding='utf-8'))