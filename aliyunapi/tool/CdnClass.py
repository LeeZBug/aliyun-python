from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest
from aliyunsdkcdn.request.v20180510.DescribeCdnDomainDetailRequest import DescribeCdnDomainDetailRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunapi.tool.Utils import serverrexception
from aliyunapi.tool.Utils import AttrDict
from aliyunapi.tool.Utils import url2domain
import json

class Cdn:
    def __init__(self, client, response_format='json'):
        """

        :param client: class type, AcsClient class. 阿里云sdk的AcsClient类，加载ak，地域信息
        :param response_format: str type, response format. 请求返回的结果格式，默认json格式
        """
        self.client = client
        self.response_format = response_format

    def add_cdn_domain(self):
        pass

    def refresh_cdn(self, domain, domainpath: str = "/"):
        """
        cdn目录刷新，默认刷新根目录
        :param domain: 需要刷新的域名
        :param domainpath: 需要刷新的目录，默认为网站的根目录
        :return:
        """
        try:
            request = RefreshObjectCachesRequest()
            request.set_accept_format(self.response_format)
            request.set_ObjectPath(domain + domainpath)
            request.set_ObjectType("Directory")
            response = self.client.do_action_with_exception(request)
            res_str = str(response, encoding='utf-8')
            if "RefreshTaskId" in res_str:
                print("网站:{0} CDN目录刷新成功".format(domain))
        except ServerException as se:
            print("刷新失败，请登录阿里云控制台进行目录刷新！")
            serverrexception(se)
            # print("详细错误信息如下：\nRequest_ID: {0}\n错误消息为: {1}\n".format(se.get_request_id(),se.get_error_msg()))

    def get_cname_info(self, speeddomain):
        request = DescribeCdnDomainDetailRequest()
        request.set_accept_format(self.response_format)
        request.set_DomainName(url2domain(speeddomain))
        response = self.client.do_action_with_exception(request)
        resstr = str(response, encoding='utf-8')
        res_json = json.loads(resstr)
        print("加速域名为:" + url2domain(speeddomain) + "\nCNAME为：" + AttrDict(AttrDict(res_json).GetDomainDetailModel).Cname)
        # print("域名:" + speeddomain + "\nCNAME为：" + res_json['GetDomainDetailModel']['Cname'])
