import time

import wx
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.AuthorizeSecurityGroupRequest import AuthorizeSecurityGroupRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceAttributeRequest import DescribeInstanceAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupAttributeRequest import DescribeSecurityGroupAttributeRequest
from aliyunsdkecs.request.v20140526.JoinSecurityGroupRequest import JoinSecurityGroupRequest

# author:lizhejie
# 已知bug：
#   1.无法查询经典网络下的实例ip信息，会导致实例列表中有经典网络实例时result窗口均显示为空白，控制台报错：
#       ip = ecs_dict["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]
#   IndexError: list index out of range
#

app = wx.App()
win = wx.Frame(None, title="阿里云工具---暂支持ECS", size=(777, 777))
win.Show()


# 创建客户端
def createclient():
    region_id = region_id_mes_command.GetValue()
    secret_id = secret_id_mes_command.GetValue()
    secret_key = secret_key_mes_command.GetValue()
    product_name = product_name_mes_command.GetValue()
    endpoint = endpoint_mes_command.GetValue()
    instanceid = instanceid_mes_command.GetValue()
    # print(region_id,secret_id,secret_key,product_name,endpoint,instanceid)
    client = AcsClient(secret_id, secret_key, region_id)
    return (region_id,
            secret_id,
            secret_key,
            product_name,
            endpoint,
            client)


# 按钮动作
def desins(event):  # 查询实例ip，加入的安全组
    region_id, secret_id, secret_key, product_name, endpoint, client = createclient()
    client.add_endpoint(region_id, product_name, endpoint)

    instanceid = instanceid_mes_command.GetValue().split(",")

    ins_info = ""
    sgid_sgn = ""
    rulelists = ""

    for ins in instanceid:
        # print(ins) 调试点
        request = DescribeInstanceAttributeRequest()
        request.set_InstanceId(ins)
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)

        # 转换字符串为字典类型
        ecs_dict = eval(str(response, encoding='utf-8'))

        # 返回实例IP，实例安全组列表
        if ecs_dict["InstanceNetworkType"] == "classic":
            ip = ecs_dict["PublicIpAddress"]["IpAddress"][0]
        else:
            ip = ecs_dict["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]
        sgid_list = ecs_dict["SecurityGroupIds"]["SecurityGroupId"]

        ins_info = ins_info + "实例ID为：" + ins + "\n实例IP为：" + ip + "\n实例安全组有：" + str(sgid_list) + "\n"

        for sgid in sgid_list:
            # print(gid)    调试点
            request = DescribeSecurityGroupAttributeRequest()
            request.set_accept_format('json')
            request.set_SecurityGroupId(sgid)
            response = client.do_action_with_exception(request)
            sec_dict = eval(str(response, encoding='utf-8'))
            sgn = sec_dict["SecurityGroupName"]
            segid = sec_dict['SecurityGroupId']
            rules = sec_dict['Permissions']['Permission']
            # print(rules) 调试点
            if not rules:
                rulelist = ins + " " + segid + " - - - - - -\n"
            for i in range(len(rules)):
                # print(i)
                SourceCidrIp = str(rules[i]['SourceCidrIp'])
                IpProtocol = str(rules[i]['IpProtocol'])
                PortRange = str(rules[i]['PortRange'])
                Policy = str(rules[i]['Policy'])
                Direction = str(rules[i]['Direction'])
                Priority = str(rules[i]['Priority'])
                if Direction == 'egress':
                    Direction = '出方向'
                    # print(instanceid, segid, Policy, Direction, IpProtocol, PortRange, SourceCidrIp, Priority) 调试点
                    rulelist = ins + " " + segid + " " + Policy + " " + Direction + " " + IpProtocol + " " + PortRange + " " + SourceCidrIp + " " + Priority + "\n"
                else:
                    Direction = '入方向'
                    # print(instanceid, segid, Policy, Direction, IpProtocol, PortRange, SourceCidrIp, Priority) 调试点
                    rulelist = ins + " " + segid + " " + Policy + " " + Direction + " " + IpProtocol + " " + PortRange + " " + SourceCidrIp + " " + Priority + "\n"
                rulelists = rulelists + rulelist
            rulelists = rulelists + rulelist
            result_text2.SetValue(rulelists)
            sgid_sgn = sgid_sgn + "安全组ID为：" + segid + "  安全组名称为：" + sgn + "\n"
            result_text1.SetValue(sgid_sgn)
    result_text0.SetValue(ins_info)


def sgname(event):  # 查询安全组名称
    region_id, secret_id, secret_key, product_name, endpoint, client = createclient()
    client.add_endpoint(region_id, product_name, endpoint)

    securitygroupids = securitygroup_mes_command.GetValue().split(",")
    # print(securitygroupids)  调试点
    sgid_sgn = ""
    rulelists = ""
    for sgid in securitygroupids:
        # print(gid)    调试点
        request = DescribeSecurityGroupAttributeRequest()
        request.set_accept_format('json')
        request.set_SecurityGroupId(sgid)
        response = client.do_action_with_exception(request)
        sec_dict = eval(str(response, encoding='utf-8'))
        sgn = sec_dict["SecurityGroupName"]
        segid = sec_dict['SecurityGroupId']
        rules = sec_dict['Permissions']['Permission']
        if not rules:
            rulelist = segid + " - - - - - -\n"

        for i in range(len(rules)):
            SourceCidrIp = str(rules[i]['SourceCidrIp'])
            IpProtocol = str(rules[i]['IpProtocol'])
            PortRange = str(rules[i]['PortRange'])
            Policy = str(rules[i]['Policy'])
            Direction = str(rules[i]['Direction'])
            Priority = str(rules[i]['Priority'])
            if Direction == 'egress':
                Direction = '出方向'
                # print(instanceid, segid, Policy, Direction, IpProtocol, PortRange, SourceCidrIp, Priority) 调试点
                rulelist = segid + " " + Policy + " " + Direction + " " + IpProtocol + " " + PortRange + " " + SourceCidrIp + " " + Priority + "\n"
            else:
                Direction = '入方向'
                # print(instanceid, segid, Policy, Direction, IpProtocol, PortRange, SourceCidrIp, Priority) 调试点
                rulelist = segid + " " + Policy + " " + Direction + " " + IpProtocol + " " + PortRange + " " + SourceCidrIp + " " + Priority + "\n"
            rulelists = rulelist + rulelists
        rulelists = rulelist + rulelists
        # rulelists = rulelist + rulelists
        result_text2.SetValue(rulelists)
        sgid_sgn = sgid_sgn + "安全组ID为：" + segid + "  安全组名称为：" + sgn + "\n"
        result_text1.SetValue(sgid_sgn)


def setwhite(event):  # 设置安全组规则
    localtime = time.asctime(time.localtime(time.time()))
    region_id, secret_id, secret_key, product_name, endpoint, client = createclient()
    client.add_endpoint(region_id, product_name, endpoint)

    request = AuthorizeSecurityGroupRequest()
    secgroupid = securitygroup_mes_command.GetValue()
    request.set_SecurityGroupId(secgroupid)
    whitelists = result_text3.GetValue().split("\n")
    # print(whitelists) 调试点

    request.set_accept_format('json')
    request.set_IpProtocol("tcp")
    # internet外网 or intranet内网
    request.set_NicType("intranet")
    request.set_Description("创建于" + localtime)
    results = ""
    for i in range(len(whitelists)):
        whitelist = tuple(whitelists[i].split(","))
        # print(whitelist)   调试点
        policy = str(whitelist[0])
        portrange = str(whitelist[1])
        sourcecidrip = str(whitelist[2])
        priority = str(whitelist[3])

        request.set_PortRange(portrange)
        request.set_SourceCidrIp(sourcecidrip)
        request.set_Policy(policy)
        request.set_Priority(priority)
        response = client.do_action_with_exception(request)
        # print(str(response, encoding="utf-8)   调试点
        result = "规则添加成功: " + policy + " " + portrange + " " + sourcecidrip + " " + priority + "\n"
        results = results + result
    result_text2.SetValue(results)


def joinseg(event):
    region_id, secret_id, secret_key, product_name, endpoint, client = createclient()
    client.add_endpoint(region_id, product_name, endpoint)

    instanceids = instanceid_mes_command.GetValue().split(",")
    securitygroupid = securitygroup_mes_command.GetValue()
    result = ""
    for ins in instanceids:
        request = JoinSecurityGroupRequest()
        request.set_InstanceId(ins)
        request.set_SecurityGroupId(securitygroupid)
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        result = ins + "," + result
    result = result + "已添加到" + securitygroupid
    result_text2.SetValue(result)


# 界面设计区域
region_id_mes = wx.StaticText(win, 1, "region_id(*)：", pos=(5, 10))
secret_id_mes = wx.StaticText(win, 2, "secret_id(*)：", pos=(5, 40))
secret_key_mes = wx.StaticText(win, 3, "secret_key(*)：", pos=(5, 70))
product_name_mes = wx.StaticText(win, 4, "产品名(*)：\n", pos=(5, 100))
endpoint_mes = wx.StaticText(win, 5, "endpoint(*)：", pos=(5, 130))
instanceid_mes = wx.StaticText(win, 6, "实例ID(*)：", pos=(5, 160))
securitygroup_mes = wx.StaticText(win, 7, "安全组ID：\n(安全组操作时必填)", pos=(5, 190))
rule_mes = wx.StaticText(win, 8, "安全组入方向规则默认tcp,内网网卡无法修改,格式为:策略,端口,源地址,优先级。多条换行", pos=(280, 10))

region_id_mes_command = wx.TextCtrl(win, 1, value="cn-hangzhou", pos=(110, 10), size=(110, 20))
secret_id_mes_command = wx.TextCtrl(win, 2, value="", pos=(110, 40), size=(250, 20))
secret_key_mes_command = wx.TextCtrl(win, 3, value="", pos=(110, 70), size=(280, 20))
product_name_mes_command = wx.TextCtrl(win, 4, value="ecs", pos=(110, 100), size=(85, 20))
endpoint_mes_command = wx.TextCtrl(win, 5, value="ecs.cn-hangzhou.aliyuncs.com", pos=(110, 130), size=(200, 20))
instanceid_mes_command = wx.TextCtrl(win, 6, value="", pos=(110, 160), size=(200, 20))
securitygroup_mes_command = wx.TextCtrl(win, 7, value="", pos=(110, 190), size=(250, 20))

# 结果保存页
result_text0 = wx.TextCtrl(win, 0, value="", pos=(5, 300), size=(750, 100), style=wx.TE_MULTILINE)
result_text1 = wx.TextCtrl(win, 1, value="", pos=(5, 410), size=(750, 80), style=wx.TE_MULTILINE)
result_text2 = wx.TextCtrl(win, 2, value="", pos=(5, 500), size=(750, 200), style=wx.TE_MULTILINE)
result_text3 = wx.TextCtrl(win, 2, value="", pos=(400, 30), size=(350, 200), style=wx.TE_MULTILINE)

# 按钮绑定
outputButton0 = wx.Button(win, label='查询实例信息', pos=(20, 250), size=(80, 25))
outputButton0.Bind(wx.EVT_BUTTON, desins)

outputButton1 = wx.Button(win, label='查询安全组名称', pos=(120, 250), size=(100, 25))
outputButton1.Bind(wx.EVT_BUTTON, sgname)

outputButton2 = wx.Button(win, label='实例移入安全组', pos=(250, 250), size=(100, 25))
outputButton2.Bind(wx.EVT_BUTTON, joinseg)

outputButton4 = wx.Button(win, label='设置安全组规则', pos=(400, 250), size=(100, 25))
outputButton4.Bind(wx.EVT_BUTTON, setwhite)

# 主程序启动
app.MainLoop()
