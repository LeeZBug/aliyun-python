from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.DescribeCdnDomainDetailRequest import DescribeCdnDomainDetailRequest
import json
from aliyunapi.tool.Utils import *

argcheck(sys.argv, 3)
sys.argv.pop(0)
"""
命令行运行需要2个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 需要刷新的域名，需要带末尾带/
"""

account, speeddomain = sys.argv
region, akid, aksrt = akconfig(account)
client = AcsClient(akid, aksrt, region)

request = DescribeCdnDomainDetailRequest()
request.set_accept_format('json')

request.set_DomainName(speeddomain)
response = client.do_action_with_exception(request)
# print(str(response, encoding='utf-8'))

resstr = str(response, encoding='utf-8')
res_json = json.loads(resstr)
print("域名:"+speeddomain+"\nCNAME为："+res_json['GetDomainDetailModel']['Cname'])

