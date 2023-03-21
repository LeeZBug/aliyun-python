import json

from aliyunsdkcdn.request.v20180510.DescribeCdnCertificateDetailRequest import DescribeCdnCertificateDetailRequest
from aliyunsdkcdn.request.v20180510.SetCdnDomainStagingConfigRequest import SetCdnDomainStagingConfigRequest
from aliyunsdkcdn.request.v20180510.SetDomainServerCertificateRequest import SetDomainServerCertificateRequest
from aliyunsdkcore.client import AcsClient

from aliyunapi.tool.Utils import *

"""
命令行运行需要2个参数，参数顺序为： 
第一个参数为：ak配置文件选项名(domainakinfo,cdnakinfo) 
第二个参数为：需要增加配置的CDN的域名，开头不需要有https://或者http://
第三个参数为：证书的名字（阿里云CDN证书控制台上，可以修改的那个名字）
"""
argcheck(sys.argv, 3)
sys.argv.pop(0)

account, speeddomain, certname = sys.argv
region, akid, aksrt = akconfig(account)
client = AcsClient(akid, aksrt, region)

get_cert_request = DescribeCdnCertificateDetailRequest()
get_cert_request.set_accept_format('json')
get_cert_request.set_CertName(certname)
get_cert_response = client.do_action_with_exception(get_cert_request)
get_cert_response_str = str(get_cert_response, encoding='utf-8')
get_cert_response_json = json.loads(get_cert_response_str)
cert_public = get_cert_response_json["Cert"]

set_cert_request = SetDomainServerCertificateRequest()
set_cert_request.set_accept_format('json')
set_cert_request.set_ServerCertificateStatus("on")
set_cert_request.set_CertType("cas")
set_cert_request.set_DomainName(speeddomain)
set_cert_request.set_CertName(certname)
set_cert_request.set_ServerCertificate(cert_public)
set_cert_request_response = client.do_action_with_exception(set_cert_request)
set_cert_request_response_str = str(set_cert_request_response)

if "RequestId" in set_cert_request_response_str:
    print("加速域名{0}增加https证书{1}完成".format(speeddomain, certname))

set_cdn_config_request = SetCdnDomainStagingConfigRequest()
sni_config_list = [{"functionArgs": [{"argName": "https_origin_sni", "argValue": speeddomain},
                                     {"argName": "enabled", "argValue": "on"}], "functionName": "https_origin_sni"}]
set_cdn_config_request.set_Functions()
set_cdn_config_request.set_DomainName("ys-mh.zjrongxiang.com")
response = client.do_action_with_exception(set_cdn_config_request)
print(str(response, encoding='utf-8'))
