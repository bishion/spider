import execjs
from urllib import request
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

"""
阿里详情页的信息是用了一段js来展示的,可以通过截取或者正则的方式将变量值拿出,但是代码会比较难看
本类使用了 python的一个js 解析器：execjs
通过它, 我们可以将阿里详情页面的二次链接返回的js解析出来
解析出来之后,我们返回的是一个字典,{"content":文本内容,"images":图片链接列表}
"""


class AliJsParser(object):
    @staticmethod
    def parseJs(url):
        response = request.urlopen(url).read().decode("gbk")

        detail_content_text = execjs.compile(response).eval('offer_details')['content']

        detail_content_html = BeautifulSoup(detail_content_text, "html.parser")

        content = detail_content_html.text
        image_links = [img["src"] for img in detail_content_html.find_all("img",src=True)]

        return {"content":content,"images":image_links}


if __name__ == '__main__':
    url = "https://img.alicdn.com/tfscom/TB1LzRVGFzqK1RjSZFoXXbfcXXa"
    print("ali_js",AliJsParser.parseJs(url))
