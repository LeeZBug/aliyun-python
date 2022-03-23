import configparser
import os
import re
import sys

from aliyunsdkcore.acs_exception.exceptions import ServerException

import aliyunapi


def checkconfigfield(optlist, field):
    """
    :param optlist:
    :param field:
    :return: bool
    """
    has_field = field in optlist
    return has_field


def akconfig(akaccount):
    """
    :param: akaccount: string
    :return: region,akid,aksrt: string
    """
    rootpath = os.path.dirname(aliyunapi.__file__)
    configfilepath = rootpath + os.sep + "config" + os.sep + "config.ini"

    cf = configparser.ConfigParser()
    cf.read(configfilepath)
    secs = cf.sections()
    # print("secs:", secs)
    if akaccount not in secs:
        print("没有找到{0}账号的配置信息!!!".format(akaccount))
        exit(1)
    options = cf.options(akaccount)  # 获取某个section名为akaccount所对应的键
    # print("options:", options)

    # items = cf.items("akaccount")  # 获取section名为akaccount所对应的全部键值对
    # print(items)

    has_regions_field = checkconfigfield(options, "region")
    has_akid_field = checkconfigfield(options, "akid")
    has_aksrt_field = checkconfigfield(options, "aksrt")
    if not has_regions_field:
        print("没有配置地区信息")
        exit(1)
    if not has_akid_field:
        print("没有配置对应账号的akid")
        exit(1)
    if not has_aksrt_field:
        print("没有配置对应账号的aksrt")
        exit(1)

    region = cf.get(akaccount, "region")
    akid = cf.get(akaccount, "akid")
    aksrt = cf.get(akaccount, "aksrt")
    return region, akid, aksrt


def argcheck(arglist, num):
    if len(arglist) < num:
        print(" argument is less！Need {0} arguments!!!".format(num - 1))
        sys.exit(1)
    else:
        pass


# 继承自dict，实现可以通过.来操作元素
class AttrDict(dict):
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __delattr__(self, item):
        self.__delitem__(item)


# 输入完整域名返回主机名和主域名
def domain_convert(fulldomain):
    index = fulldomain.find('.')
    hostname = fulldomain[0:index]
    domainname = fulldomain[index + 1:]
    return hostname, domainname


# 输入主机名和主域名，返回完整域名
def convert_domain(hostname, domainname):
    return hostname + '.' + domainname


# 通用简洁的异常信息
def serverrexception(se: ServerException):
    print("详细错误信息如下：\nRequest_ID: {0}\nError Code: {1}\nError Message: {2}\n错误解释点击 https://error-center.aliyun.com/"
          .format(se.get_request_id(), se.get_error_code(), se.get_error_msg()))


# 输入带协议的网址，返回域名
def schemeurl2domain(url):
    start, end = re.search(r'^[a-zA-z]+://', url).span()
    return url[end:]


# 错误信息拼接并打印
def print_error_message(requestid: str = '', code: str = '', message: str = '', recommend: str = ''):
    print("RequestId: {0}\nCode: {1}\nMessage: {2}\nRecommend: {3}\n".format(requestid, code, message, recommend))


if __name__ == '__main__':
    # region, akid, aksrt = akconfig("domainakinfo")
    # print("#####account akinfo#######:\nregion:{0}\nakid:{1}\naksrt:{2}\n".format(region, akid, aksrt))
    # print(domain_convert('www.zjrongxiang.com'))
    print(schemeurl2domain("https://test.lizhejie.com"))
