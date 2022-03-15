from aliyunapi.tool.Utils import domain_convert
from aliyunapi.tool.Utils import AttrDict
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest
import json


class DnsRecord:
    def __init__(self, client, response_format='json'):
        self.client = client
        self.response_format = response_format

    def get_dns_info(self, fulldomain='', pagenumber=1, pagesize=200):
        hostname, domainname = domain_convert(fulldomain=fulldomain)
        request = DescribeDomainRecordsRequest()
        request.set_accept_format(self.response_format)
        request.set_DomainName(domainname)
        request.set_PageNumber(pagenumber)
        request.set_PageSize(pagesize)
        response = self.client.do_action_with_exception(request)
        res_str = str(response, encoding='utf-8')
        res_json = json.loads(res_str)
        res_recordlist = AttrDict(AttrDict(res_json).DomainRecords).Record

        find_flag = 0
        for i in range(len(res_recordlist)):
            if res_recordlist[i]["RR"] == hostname:
                find_flag = 1
                print("记录ID为： " + res_recordlist[i]["RecordId"])
                print("记录状态为： " + res_recordlist[i]["Status"])
                print("记录主机名为： " + res_recordlist[i]["RR"])
                print("记录类型为： " + res_recordlist[i]["Type"])
                print("记录值为： " + res_recordlist[i]["Value"], end='\n\n')
        if not find_flag:
            # 只表示在调用的第n页的全m条记录中不存在。不表示所有记录中不存在。
            print("未找到该域名解析记录")
            return False

    def add_dns_record(self, rr, recordtype, domain, value):
        request = AddDomainRecordRequest()
        request.set_accept_format(self.response_format)
        request.set_DomainName(domain)
        request.set_RR(rr)
        request.set_Type(recordtype)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        if "RecordId" in str(response, encoding='utf-8'):
            print("DNS记录已增加，主机名{0}，记录类型{1}，记录值{2}".format(rr, recordtype, value))
            print("完整域名为：" + rr + domain)

    def del_dns_record(self, record_id):
        pass

    def change_record_status(self):
        pass






