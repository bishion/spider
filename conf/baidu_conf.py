import configparser
import json
import time
import urllib
from urllib import request

baidu_token_time = 30 * 24 * 3600
baidu_token_url = "https://aip.baidubce.com/oauth/2.0/token"


class BaiduTokenService(object):
    def __init__(self):
        self.token = None

    """
       这个方法比较绕.
       背景：
       1. 百度的接口需要拿key去换token, 一个token 30天过期
       2. 牵涉到配置key信息,所以我需要将配置文件放到本地而不是代码中.
       3. 百度的key 30天才过期, 我可以存到本地, 大约30天拿一次就可以

       解决方法：
       1. 将配置文件放到本地
       2. 配置文件初始化记录key, 为了程序处理方便,也会将token 初始化为任意值
       3. 配置文件中记录上一次token更新的时间,如果已经大于30天了,那就再更新一次
       """
    def get_baidu_token(self):
        if self.token:
            return self.token
        conf = configparser.ConfigParser()
        conf.read("/home/bishion/ocr.ini")
        api_key = conf.get("baidu", "api_key")
        secret_key = conf.get("baidu", "secret_key")
        self.token = conf.get("baidu", "token")
        # 获取上次更新时间, 如果在30天内,那就不更新,否则就更新
        modify_time = conf.getfloat("baidu", "modify_time")

        now = time.time()
        if now - modify_time > baidu_token_time:
            self.token = BaiduTokenService.request_for_token(api_key, secret_key)

            conf.set("baidu", "modify_time", str(now))
            conf.set("baidu", "token", self.token)
            with open("/home/bishion/ocr.ini", "w") as configfile:
                conf.write(configfile)
        return self.token

    @staticmethod
    def request_for_token(api_key, secret_key):
        parameter = {"client_id": api_key, "client_secret": secret_key, "grant_type": "client_credentials"}
        data = bytes(urllib.parse.urlencode(parameter), encoding="utf-8")
        token_result = request.urlopen(baidu_token_url, data=data).read().decode("unicode_escape")
        result_obj = json.loads(token_result, encoding="utf-8", strict=False)
        return result_obj["access_token"]


baidu_token_service = BaiduTokenService()
