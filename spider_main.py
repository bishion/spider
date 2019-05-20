from web_site.ali_shop.ali_shop_service import AliShopService
if __name__ == '__main__':

    yxrywy = AliShopService("https://yxrywy8.1688.com/page/offerlist.htm")

    yxrywy.check_jixianci()