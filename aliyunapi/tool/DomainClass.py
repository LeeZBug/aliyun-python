import json

from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest

from aliyunapi.tool.Utils import AttrDict
from aliyunapi.tool.Utils import convert_domain
from aliyunapi.tool.Utils import domain_convert


class DnsRecord:
    def __init__(self, client, response_format='json'):
        """

        :param client: class type, AcsClient class. 阿里云sdk的AcsClient类，加载ak，地域信息
        :param response_format: str type, response format. 请求返回的结果格式，默认json格式
        """
        self.client = client
        self.response_format = response_format

    def get_dnsinfo_by_domain(self, fulldomain: str = '', pagenumber: int = 1, pagesize: int = 200):
        """
        通过完整域名获得DNS记录详细信息
        :param fulldomain: str type, include hostname,netname. 完整域名，包含主机名和网络名，如www.baidu.com
        :param pagenumber: int type. 请求第几页
        :param pagesize: int type. 请求每页包含多少条记录
        :return:
        """
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

    def get_dnsinfo_by_id(self, record_id: str):
        """
        通过DNS记录id获得记录详细信息
        :param record_id: DNS's record_id, func get_dns_info can return dns record info
        :return:
        """
        request = DescribeDomainRecordInfoRequest()
        request.set_accept_format(self.response_format)
        request.set_RecordId(str(record_id))
        response = self.client.do_action_with_exception(request)
        res_str = str(response, encoding='utf-8')
        res_json = json.loads(res_str)

        print("记录ID为： " + AttrDict(res_json).RecordId)
        print("记录状态为： " + AttrDict(res_json).Status)
        print("记录主机名为： " + AttrDict(res_json).RR)
        print("记录类型为： " + AttrDict(res_json).Type)
        print("记录值为： " + AttrDict(res_json).Value)
        print("完整域名为： " + convert_domain(AttrDict(res_json).RR, AttrDict(res_json).DomainName), end='\n\n')

    def add_dns_record(self, rr: str, record_type: str, domain: str, value: str):
        """
        增加DNS记录
        :param rr: str type, DNS record's hostname. DNS记录的主机记录
        :param record_type: str type, DNS record's record type. options: A,CNAME,TXT... DNS记录的记录类型，可选A，CANME...
        :param domain: str type, DNS record's netname. DNS记录的域名名称
        :param value: str type, DNS record's record value.
        :return:
        """
        request = AddDomainRecordRequest()
        request.set_accept_format(self.response_format)
        request.set_DomainName(domain)
        request.set_RR(rr)
        request.set_Type(record_type)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        if "RecordId" in str(response, encoding='utf-8'):
            print("DNS记录已增加，主机名{0}，记录类型{1}，记录值{2}".format(rr, record_type, value))
            fulldomain = convert_domain(rr, domain)
            print("完整域名为：" + fulldomain)
            res_str = str(response, encoding='utf-8')
            res_json = json.loads(res_str)
            record_id = AttrDict(res_json).RecordId
            print("该条记录的RecordID为："+record_id)

    def del_dns_record(self, record_id: str):
        """
        删除DNS记录
        :param record_id: DNS's record_id, func get_dns_info can return dns record info
        :return:
        """
        # 在删除前先打印记录的详细信息
        self.get_dnsinfo_by_id(record_id)
        request = DeleteDomainRecordRequest()
        request.set_accept_format(self.response_format)
        request.set_RecordId(str(record_id))
        response = self.client.do_action_with_exception(request)
        res_str = str(response, encoding='utf-8')
        res_json = json.loads(res_str)
        print("删除的记录ID为： " + AttrDict(res_json).RecordId)

    def change_record_status(self, record_id: str, status: str):
        """
        DNS记录是否启动
        :param record_id: str type. DNS's record_id, func get_dns_info can return dns record info
        :param status: str type, Disable or Enable
        :return:
        """
        request = SetDomainRecordStatusRequest()
        request.set_accept_format(self.response_format)
        request.set_RecordId(record_id)
        request.set_Status(status)
        response = self.client.do_action_with_exception(request)
        res_str = str(response, encoding='utf-8')
        res_json = json.loads(res_str)
        print("更改状态的记录ID为： " + AttrDict(res_json).RecordId)
        print("状态更改为： " + AttrDict(res_json).Status)
        self.get_dnsinfo_by_id(record_id)
