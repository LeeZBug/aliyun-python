from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import sys
import time
from aliyunapi.tool.Utils import *
"""
大概率无法增加TXT类型解析后，无法自动提交审核，需要手动去阿里云控制台-证书管理进行手动提交审核
得到的公私钥文件每行后面可能存在大量空格，会导致文件无效
"""


# 检查免费证书资源包使用数量
def describe_resouce():
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('cas.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2020-04-07')
    request.set_action_name('DescribePackageState')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('ProductCode', "symantec-free-1-free")

    response = client.do_action(request)
    res_dict = json.loads(response)
    free_total_cert = res_dict['TotalCount']
    usedcount = res_dict['UsedCount']
    available_count = free_total_cert - usedcount
    print("##### SSL申请概况 #####\n可申请面免费证书总数：{0}\n已申请免费证书：{1}\n当前可申请免费证书个数：{2}\n".format(
        free_total_cert, usedcount, available_count))


# 提交证书申请
def create_cert_request(domain):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('cas.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2020-04-07')
    request.set_action_name('CreateCertificateForPackageRequest')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('ProductCode', "symantec-free-1-free")
    request.add_query_param('Domain', domain)  # 替换需要申请的域名
    request.add_query_param('ValidateType', "DNS")

    response = client.do_action(request)
    res_dict = json.loads(response)
    orderid = res_dict['OrderId']
    return str(orderid)


# 查看DNS验证的TXT类型的解析详细信息
def describe_cert_state_before(ordid):
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
    # print(str(response, encoding='utf-8'))
    res_dict = json.loads(response)
    recordtype = res_dict['RecordType']
    recordomain = res_dict['RecordDomain']
    recordvalue = res_dict['RecordValue']
    # 证书未被DNS验证和审核通过则返回DNS验证的记录信息，主机
    return recordomain, recordtype, recordvalue


# 查看DNS验证通过后的公钥和私钥内容
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

    describe_resouce()
    # domain = "testdomain.zjrongxiang.com"
    domain = sys.argv[2]
    # 订单号也可以在阿里云ssl证书的实例名称看到。cert-xxxxxx
    # ordid = "6132930"
    ordid = create_cert_request(domain)
    # 需要等待上一个请求在阿里服务器完成才能describe_cert_state，否则会出现type unknow.故增加sleep
    time.sleep(5)
    recordomain, recordtype, recordvalue = describe_cert_state_before(ordid)
    recordomainlist = str(recordomain).split('.')
    recordomainhost = recordomainlist[0] + '.' + recordomainlist[1]
    print("正在申请证书的域名为：{0}".format(domain))
    print("此次申请证书的订单ID为：{0}".format(ordid))
    print("#####需要添加的解析记录如下#####\n主机记录：{0}\n记录类型：{1}\n记录值：{2}\n".format(recordomainhost, recordtype, recordvalue))
    domain_certfile = domain+".pem"
    domain_key = domain+".key"
    print("证书已申请，等待验证结果（600s内未返回构建会失败但不影响阿里云上继续审核证书的结果）")
    is_certificate = False
    timedur = 0
    while True:
        is_certificate = describe_cert_state_after(ordid)
        if timedur == 600 or is_certificate:
            break
        time.sleep(30)
        timedur += 30
