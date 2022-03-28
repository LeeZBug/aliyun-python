from oss2 import Auth, Bucket


class OssService(Bucket):
    def __init__(self, region: str, akid: str, aksrt: str, bucketname: str):
        self.endpoint = "oss-" + region + ".aliyuncs.com"
        self.auth = Auth(akid, aksrt)
        super(OssService, self).__init__(self.auth, self.endpoint, bucketname)

    def put_object2oss(self, ossfile: str, localfile: str):
        super(OssService, self).put_object_from_file(key=ossfile, filename=localfile)

    def get_object4oss(self, ossfile: str, localfile: str):
        super(OssService, self).get_object_to_file(key=ossfile, filename=localfile)
