import configparser
import aliyunapi
import sys
import os


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
        print("没有配置对应账号的akscr")
        exit(1)

    region = cf.get(akaccount, "region")
    akid = cf.get(akaccount, "akid")
    aksrt = cf.get(akaccount, "aksrt")
    return region, akid, aksrt


def argcheck(arglist, num):
    if len(arglist) < num:
        print(" argument is less！Need {0} arguments!!!".format(num-1))
        sys.exit(1)
    else:
        pass


if __name__ == '__main__':
    region, akid, aksrt = akconfig("domainakinfo")
    print("#####account akinfo#######:\nregion:{0}\nakid:{1}\naksrt:{2}\n".format(region, akid, aksrt))
