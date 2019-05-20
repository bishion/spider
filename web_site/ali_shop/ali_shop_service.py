import traceback

from service.product_service import ProductService
from web_site.ali_shop.shop_spider import ShopSpider


class AliShopService(object):

    @staticmethod
    def check_jixianci(main_url):
        check_result = []
        # 获取所有商品链接
        # all_links = ShopSpider().get_all_links_by_first_page(main_url)

        all_links = ["https://detail.1688.com/offer/562007279823.html"]
        # 迭代爬取所有商品,并逐一校验
        for item in all_links:
            try:
                product_check_result = ProductService.check_product(ShopSpider.craw_product_info(item))
                if product_check_result:
                    print(product_check_result)
                    check_result.append(product_check_result)
            except Exception as e:
                print(item, e)
                traceback.print_exc()

    @staticmethod
    def show_result(result_list):
        if not result_list:
            print("数据为空")
            return
        for result in result_list:
            print(result)
