import re
from urllib import request
from bs4 import BeautifulSoup

from dto.product import Product


class ShopSpider(object):
    def __init__(self):
        self.__all_links = set()

    def __craw_by_page(self, current_page_url):
        # 如果当前的 url 不合法,就返回
        if not re.match(r'^https?:/{2}\w.+$', current_page_url):
            return
        current_page_text = request.urlopen(current_page_url)
        current_page_html = BeautifulSoup(current_page_text, "html.parser")
        # 获取当前页面的产品列表
        self.__parse_product_in_page(current_page_html)

        # 获取下一页的url,然后再获取下一页的产品列表
        next_page_tag = current_page_html.find("a", class_="next")

        # 最后一页的时候, 没有next的节点了
        if next_page_tag:
            self.__craw_by_page(next_page_tag["href"])
        return

    def __parse_product_in_page(self, current_page_html):
        for li in current_page_html.find_all("li", class_="offer-list-row-offer"):
            link = li.find("a")["href"]
            self.__all_links.add(link)

    def get_all_links_by_first_page(self, first_page_url):
        self.__craw_by_page(first_page_url)
        return self.__all_links

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
        detail_content = ShopSpider.parseJs(detail_url)
        return Product(product_url, title, head, detail_content["content"], detail_content["images"], detail_url)
