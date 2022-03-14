from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest
import sys
import json
from aliyunapi.tool.Utils import *

argcheck(sys.argv, 3)
"""
命令行运行需要3个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 全域名：主机记录.主域名
第3个为可选参数，是否开启解析：Enable 或 Disable
"""
account = sys.argv[1]
fulldomain = sys.argv[2]
status = ''
if len(sys.argv) == 4:
    status = sys.argv[3]
index = fulldomain.find('.')
record = fulldomain[0:index]
domain = fulldomain[index+1:]

region, akid, aksrt = akconfig(account)
# print(region, akid, aksrt)
client = AcsClient(akid, aksrt, region)

request = DescribeDomainRecordsRequest()
request.set_accept_format('json')
request.set_DomainName(domain)
request.set_PageSize("200")
# for i in range(10):

request.set_PageNumber("1")
response = client.do_action_with_exception(request)

resstr = str(response, encoding='utf-8')
res_json = json.loads(resstr)
res_recordlist = AttrDict(AttrDict(res_json).DomainRecords).Record

NOTFIND_FLAG = 1
RecordId = ''
for i in range(len(res_recordlist)):
    if res_recordlist[i]["RR"] == record:
        NOTFIND_FLAG = 0
        print("记录ID为： "+res_recordlist[i]["RecordId"])
        RecordId = res_recordlist[i]["RecordId"]
        print("记录状态为： "+res_recordlist[i]["Status"])
        print("记录主机名为： "+res_recordlist[i]["RR"])
        print("记录类型为： "+res_recordlist[i]["Type"])
        print("记录值为： "+res_recordlist[i]["Value"])
        break
if NOTFIND_FLAG:
    print("未找到该域名解析记录")

if status != '' and RecordId != '':
    request = SetDomainRecordStatusRequest()
    request.set_accept_format('json')

    request.set_RecordId(RecordId)
    request.set_Status(status)

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))

