from web_site.ali_shop.ali_shop_service import AliShopService
if __name__ == '__main__':
    main_url = "https://shop52798901llv53.1688.com/page/offerlist.htm"
    # main_url = "https://yxrywy8.1688.com/page/offerlist.htm"
    result_list = AliShopService.check_jixianci(main_url)

    AliShopService.show_result(result_list)
