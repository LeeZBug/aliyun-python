from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.StopCdnDomainRequest import StopCdnDomainRequest
from aliyunsdkcdn.request.v20180510.StartCdnDomainRequest import StartCdnDomainRequest
from aliyunsdkcdn.request.v20180510.DeleteCdnDomainRequest import DeleteCdnDomainRequest
import sys
import time
from aliyunapi.tool.Utils import *

argcheck(sys.argv, 3)
sys.argv.pop(0)
"""
命令行运行需要2个参数，参数顺序为： ak配置文件选项名(domainakinfo,cdnakinfo), 操作的加速域名，如xxx.xxx.com
"""

account, acceleratedomain, status = sys.argv
region, akid, aksrt = akconfig(account)
client = AcsClient(akid, aksrt, region)

if status == "stop":
    print("即将停止加速域名:{0}，你有10秒钟可以思考是否输入正确".format(acceleratedomain))
    time.sleep(10)
    stop_request = StopCdnDomainRequest()
    stop_request.set_accept_format('json')
    stop_request.set_DomainName(acceleratedomain)
    stop_response = client.do_action_with_exception(stop_request)
    if "RequestId" in str(stop_response, encoding='utf-8'):
        print("网站:{0} CDN停用成功".format(acceleratedomain))
    else:
        print("加速域名已停用或停用失败！请登录阿里云控制台进行操作！")
        exit(1)
elif status == "start":
    print("即将启用加速域名:{0}".format(acceleratedomain))
    start_request = StartCdnDomainRequest()
    start_request.set_accept_format('json')
    start_request.set_DomainName(acceleratedomain)
    start_response = client.do_action_with_exception(start_request)
    if "RequestId" in str(start_response, encoding='utf-8'):
        print("网站:{0} CDN启用成功".format(acceleratedomain))
    else:
        print("加速域名已启用或不存在，启用失败！请登录阿里云控制台进行操作！")
        exit(1)
elif status == "delete":
    # 没有停止的话使用API接口依然可以删除，控制台无法直接删除正启用的加速域名
    print("即将删除加速域名:{0}，你有10秒钟可以思考是否输入正确".format(acceleratedomain))
    time.sleep(10)
    delete_request = DeleteCdnDomainRequest()
    delete_request.set_accept_format('json')
    delete_request.set_DomainName(acceleratedomain)
    delete_response = client.do_action_with_exception(delete_request)
    # print(str(delete_response, encoding='utf-8'))
    if "RequestId" in str(delete_response, encoding='utf-8'):
        print("网站:{0} CDN加速域名删除成功".format(acceleratedomain))
    else:
        print("加速域名已删除，启用失败！请登录阿里云控制台进行操作！")
        exit(1)


