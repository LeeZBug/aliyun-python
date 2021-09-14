from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import sys
import time
from aliyunapi.tool.Utils import *


def describe_cert_state_after(ordid):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('cas.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2020-04-07')
    request.set_action_name('DescribeCertificateState')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('OrderId', ordid)

    response = client.do_action(request)
    res_dict = json.loads(response)
    if "Type" not in res_dict:
        print("证书申请在阿里云控制台上已被取消！！！")
        exit(1)
    if res_dict['Type'] == "certificate":
        print(domain + "证书已经验证完毕并签署，")
        certificate = res_dict['Certificate']
        privatekey = res_dict['PrivateKey']
        print("######公钥内容如下：\n{0}\n\n######私钥内容如下:\n{1}".format(certificate, privatekey))
        with open(domain_certfile, "w") as cert:
            cert.write(certificate)
        with open(domain_key, "w") as key:
            key.write(privatekey)
        print("公私钥已经生成文件")
        return True
    elif res_dict['Type'] == "process":
        print("证书申请正在审核中！")
        return False
    elif res_dict['Type'] == "domain_verify":
        print("证书申请待验证！！")
        return False
    elif res_dict['Type'] == "verify_fail":
        print("证书申请审核失败！！！")
        return False
    else:
        print("证书申请为待申请或状态不正确！！！")
        exit(1)
        return False


if __name__ == '__main__':
    argcheck(sys.argv, 2)
    account = sys.argv[1]
    """
    命令行运行需要2个参数顺序为：ak配置文件选项名(domainakinfo,cdnakinfo)， 申请证书的域名
    """
    region, akid, aksrt = akconfig(account)
    # print(region, akid, aksrt)
    client = AcsClient(akid, aksrt, region)
    domain_certfile = domain+".pem"
    domain_key = domain+".key"
    is_certificate = False
    timedur = 0
    while True:
        is_certificate = describe_cert_state_after(ordid)
        if timedur == 600 or is_certificate:
            break
        time.sleep(30)
        timedur += 30