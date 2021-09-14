from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.AddCdnDomainRequest import AddCdnDomainRequest
import sys
from aliyunapi.tool.Utils import *

source1 = '[{"content": "114.114.114.114", "type": "ipaddr", "priority": "20", "port": 80, "weight": "15"},'
source2 = '{"content": "114.114.114", "type": "ipaddr", "priority": "20", "port": 80, "weight": "15"},'
source3 = '{"content": "114.114.114", "type": "ipaddr", "priority": "20", "port": 80, "weight": "15"}]'
sources = source1 + source2 + source3


argcheck(sys.argv, 3)
sys.argv.pop(0)
"""
命令行运行需要2个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 需要假如CDN的域名，开头不需要有https://或者http://
"""
account, speeddomain = sys.argv
region, akid, aksrt = akconfig(account)
client = AcsClient(akid, aksrt, region)


request = AddCdnDomainRequest()
request.set_accept_format('json')

request.set_CdnType("web")
request.set_DomainName(speeddomain)
request.set_Sources(sources)

response = client.do_action_with_exception(request)
# print(str(response, encoding='utf-8'))
res_str = str(response, encoding='utf-8')
if "RequestId" in res_str:
    print("加速域名{0}添加成功进入阿里云审核状态，暂时需要到阿里云控制台进行其余操作".format(speeddomain))
