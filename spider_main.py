from web_site.ali_shop.ali_shop_service import AliShopService
if __name__ == '__main__':

    result_list = AliShopService.check_jixianci("https://yxrywy8.1688.com/page/offerlist.htm")

    AliShopService.show_result(result_list)
