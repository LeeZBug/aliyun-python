import json
import time

from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest
from aliyunsdkcore.client import AcsClient

from aliyunapi.tool.Utils import *

argcheck(sys.argv, 3)
sys.argv.pop(0)
"""
命令行运行需要3个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 全域名：主机记录.主域名
第3个为可选参数，是否开启解析：Desc，Enable 或 Disable，不是以上三个值直接会查询域名解析
"""


def modify_dns_status(status, recorid):
    if status == 'Disable' and recorid != '':
        print("即将暂停以上解析记录!")
    if Status == 'Enable' and RecordId != '':
        print("即将启用以上解析记录！")
    set_dns_request = SetDomainRecordStatusRequest()
    set_dns_request.set_accept_format('json')

    set_dns_request.set_RecordId(RecordId)
    set_dns_request.set_Status(status)

    set_dns_response = client.do_action_with_exception(set_dns_request)
    # print(str(set_dns_response, encoding='utf-8'))
    if 'Status' in str(set_dns_response, encoding='utf-8'):
        set_dns_dict = AttrDict(json.loads(str(set_dns_response, encoding='utf-8')))
        print("RecordID：{0}的DNS解析记录当前状态为：{1}".format(recorid, set_dns_dict.Status))


account, FULLDOMAIN, Status = sys.argv

index = FULLDOMAIN.find('.')
record = FULLDOMAIN[0:index]
domain = FULLDOMAIN[index + 1:]

region, akid, aksrt = akconfig(account)
# print(region, akid, aksrt)
client = AcsClient(akid, aksrt, region)

desc_dns_request = DescribeDomainRecordsRequest()
desc_dns_request.set_accept_format('json')
desc_dns_request.set_DomainName(domain)
# 分页参数，记录值较多的时候需要修改逻辑进行循环查找
desc_dns_request.set_PageNumber("1")
desc_dns_request.set_PageSize("250")
desc_dns_response = client.do_action_with_exception(desc_dns_request)

resstr = str(desc_dns_response, encoding='utf-8')
desc_dns_response_json = json.loads(str(desc_dns_response, encoding='utf-8'))
desc_dns_res_recordlist = AttrDict(AttrDict(desc_dns_response_json).DomainRecords).Record

NOTFIND_FLAG = 1
RecordId = ''
for i in range(len(desc_dns_res_recordlist)):
    if desc_dns_res_recordlist[i]["RR"] == record:
        NOTFIND_FLAG = 0
        print("记录ID为： " + desc_dns_res_recordlist[i]["RecordId"])
        RecordId = desc_dns_res_recordlist[i]["RecordId"]
        print("记录状态为： " + desc_dns_res_recordlist[i]["Status"])
        print("记录主机名为： " + desc_dns_res_recordlist[i]["RR"])
        print("记录类型为： " + desc_dns_res_recordlist[i]["Type"])
        print("记录值为： " + desc_dns_res_recordlist[i]["Value"])
        break
if NOTFIND_FLAG:
    print("未找到该域名解析记录，记录可能在不同分页上需要修改源码")
    exit(1)

if Status == 'Desc':
    print("需要查找的域名记录信息如上")

if (Status == 'Enable' or Status == 'Disable') and RecordId != '':
    modify_dns_status(Status, RecordId)

if Status == 'Delete' and RecordId != '':
    print("即将删除的DNS记录ID为:{0}，你有10秒钟可以思考是否输入正确".format(RecordId))
    time.sleep(10)
    del_dns_request = DeleteDomainRecordRequest()
    del_dns_request.set_accept_format('json')
    del_dns_request.set_RecordId(RecordId)

    del_dns_response = client.do_action_with_exception(del_dns_request)
    # print(str(del_dns_response, encoding='utf-8'))
    if 'RecordId' in str(del_dns_response, encoding='utf-8'):
        print("RecordID为{0}的DNS解析记录删除".format(RecordId))
