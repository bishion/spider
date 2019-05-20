import re,traceback
from urllib import request

from bs4 import BeautifulSoup

from web_site.ali_shop.ali_js_parser import AliJsParser
from dto.product import Product
from service.product_service import ProductService


class AliShopService(object):
    def __init__(self,main_url):
        self.main_url = main_url
        self.all_links = set()

    @staticmethod
    def craw_product_info(product_url):
        if product_url is None:
            return
        product_text = request.urlopen(product_url)
        # get product html

        product_html = BeautifulSoup(product_text, "html.parser")
        [s.extract() for s in product_html('script')]
        # search for head product main info
        title = product_html.find("div", id="mod-detail-hd").text.replace("\n", "").replace("\t", " ")[19:]
        head = product_html.find("div", id="mod-detail-bd").text.replace("\n", "").replace("\t", "")
        # search for detail info
        detail_html = product_html.find("div", id="desc-lazyload-container")
        if detail_html is None:
            return Product(product_url, title, head)

        # detail info url
        detail_url = detail_html["data-tfs-url"]
        detail_content = AliJsParser.parseJs(detail_url)
        return Product(product_url, title, head, detail_content["content"], detail_content["images"],detail_url)

    def craw_by_pages(self, current_page_url):
        # 如果当前的 url 不合法,就返回
        if not re.match(r'^https?:/{2}\w.+$', current_page_url):
            return
        current_page_text = request.urlopen(current_page_url)
        current_page_html = BeautifulSoup(current_page_text, "html.parser")
        # 获取当前页面的产品列表
        self.parse_product_in_page(current_page_html)
        # 获取下一页的url,然后再获取下一页的产品列表
        next_page_tag = current_page_html.find("a", class_="next")
        # 最后一页的时候, 没有next的节点了
        if next_page_tag:
            self.craw_by_pages(next_page_tag["href"])
        return

    def parse_product_in_page(self, current_page_html):
        for li in current_page_html.find_all("li", class_="offer-list-row-offer"):
            link = li.find("a")["href"]
            self.all_links.add(link)

    def check_jixianci(self):
        # 获取所有商品链接
        self.craw_by_pages(self.main_url)
        # self.all_links.add("https://detail.1688.com/offer/562007279823.html")
        # 迭代爬取所有商品,并逐一校验
        for item in self.all_links:
            try:
                product_check_result = ProductService.check_product(AliShopService.craw_product_info(item))
                if product_check_result:
                    print(product_check_result)
            except Exception as e:
                print(item, e)
                traceback.print_exc()
