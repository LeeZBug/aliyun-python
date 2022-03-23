import json

from aliyunsdkcore.request import CommonRequest

from aliyunapi.tool.Utils import AttrDict, print_error_message


class Cert:
    def __init__(self, client, response_format='json'):
        """

        :param client: class type, AcsClient class. 阿里云sdk的AcsClient类，加载ak，地域信息
        :param response_format: str type, response format. 请求返回的结果格式，默认json格式
        """
        self.client = client
        self.response_format = response_format

    def get_free_cert_numb(self):
        """
        获取账号下可申请的免费证书的剩余个数,地域选择暂时未使用变量，只支持杭州地区
        :return:
        """
        request = CommonRequest()
        request.set_accept_format(self.response_format)
        request.set_domain('cas.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2020-04-07')
        request.set_action_name('DescribePackageState')
        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('ProductCode', "symantec-free-1-free")
        response = self.client.do_action(request)
        res_dict = AttrDict(json.loads(response, encoding='utf-8'))
        # AK没有权限等其他错误,显示错误
        if 'TotalCount' in res_dict:
            free_total_cert = res_dict.TotalCount
            usedcount = res_dict.UsedCount
            available_count = free_total_cert - usedcount
            print("##### SSL申请概况 #####\n可申请面免费证书总数：{0}\n已申请免费证书：{1}\n当前可申请免费证书个数：{2}\n".format(
                free_total_cert, usedcount, available_count))
        else:
            print_error_message(res_dict.RequestId, res_dict.Code, res_dict.Message, res_dict.Recommend)

    def create_cert_request(self, domain: str = ''):
        """
        提交免费证书申请
        :param domain: str type, 需要申请免费证书的域名
        :return: str type, orderid.查询证书验证类型信息时需要
        """
        if domain:
            request = CommonRequest()
            request.set_accept_format(self.response_format)
            request.set_domain('cas.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('https')
            request.set_version('2020-04-07')
            request.set_action_name('CreateCertificateForPackageRequest')
            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('ProductCode', "symantec-free-1-free")
            request.add_query_param('Domain', domain)  # 替换需要申请的域名
            request.add_query_param('ValidateType', "DNS")
            response = self.client.do_action(request)
            res_dict = AttrDict(json.loads(response, encoding='utf-8'))
            orderid = str(res_dict.OrderId)
            print("Cert's Order_Id:"+orderid+"\nDomain is:"+domain)
            return orderid
        else:
            print("You should input domain!")
