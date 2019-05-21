import requests
import traceback

from conf.baidu_conf import baidu_token_service

"""
该类主要通过百度的ocr接口将图片中的文字返回
"""
GENERAL_BASIC_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"


class BaiduOcr(object):

    @staticmethod
    def read_image_words(url):
        parameter = {"access_token": baidu_token_service.get_baidu_token(), "url": url}
        header = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(GENERAL_BASIC_URL, data=parameter,
                                 headers=header).json()
        pic_text = ""

        if "error_code" in response:
            print("图片请求报错. url:", url, "报错代码:", response["error_code"], "报错信息:", response["error_msg"])
            return None

        try:
            for line in response["words_result"]:
                # 因为图片中文字排列的不确定性，所以行与行之间不用空格而是直接相连
                pic_text = pic_text + line["words"] + ""
        except Exception as e:
            print(url, e)
            traceback.print_exc()

        return pic_text


if __name__ == '__main__':
    result = BaiduOcr().read_image_words("https://cbu01.alicdn.com/img/ibank/2014/948/696/1298696849_736701904.jpg")
    print("ocr:", result)
