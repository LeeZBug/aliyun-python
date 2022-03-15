from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkcdn.request.v20141111.SetDomainServerCertificateRequest import SetDomainServerCertificateRequest
from aliyunapi.tool.Utils import *

argcheck(sys.argv, 3)
sys.argv.pop(0)
"""
命令行运行需要2个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 需要假如CDN的域名，开头不需要有https://或者http://
"""
account, speeddomain = sys.argv
region, akid, aksrt = akconfig(account)
client = AcsClient(akid, aksrt, region)

request = SetDomainServerCertificateRequest()
request.set_accept_format('json')

request.set_ServerCertificateStatus("on")
request.set_DomainName(speeddomain)
# cas参数为使用证书中心的ssl证书
request.set_CertType("cas")
# 证书名，在证书中心中的证书名称
request.set_CertName("xxx")

response = client.do_action_with_exception(request)
print(str(response, encoding='utf-8'))


