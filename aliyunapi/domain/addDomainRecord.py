from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
import sys
from aliyunapi.tool.Utils import *


argcheck(sys.argv, 5)
"""
命令行运行需要4个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 主机记录， 记录类型，记录值。调用只在在zjrongxiang.com的域上进行添加二级域名
"""
account, rr, recordtype, value = sys.argv[1:5]
# print(account, rr, recordtype, value)

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
if "RecordId" in str(response, encoding='utf-8'):
    print("DNS记录已增加，主机名{0}，记录类型{1}，记录值{2}".format(rr, recordtype, value))
    print("完整域名为："+rr+".zjrongxiang.com")
