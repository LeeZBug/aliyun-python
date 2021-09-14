from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest
import sys
from aliyunapi.tool.Utils import *

argcheck(sys.argv, 3)
sys.argv.pop(0)
"""
命令行运行需要2个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 需要刷新的域名，需要带末尾带/
"""

account, domain = sys.argv
region, akid, aksrt = akconfig(account)
client = AcsClient(akid, aksrt, region)

request = RefreshObjectCachesRequest()
request.set_accept_format('json')

request.set_ObjectPath(domain)
request.set_ObjectType("Directory")

response = client.do_action_with_exception(request)
# print(str(response, encoding='utf-8'))
res_str = str(response, encoding='utf-8')
if "RefreshTaskId" in res_str:
    print("网站:{0} CDN目录刷新成功".format(domain))
else:
    print("刷新失败，请登录阿里云控制台进行目录刷新！")
    exit(1)

