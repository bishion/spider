from dto.product import Product


class CheckResultDTO(object):
    def __init__(self, product: Product, title_result, head_result, content_result, image_result):
        self.product = product
        if title_result is not None and head_result is not None and image_result is not None and content_result is not None:
            self.all_pass = True
            return
        self.all_pass = False
        self.title_result = title_result
        self.head_result = head_result
        self.content_result = content_result
        self.image_result = image_result

    def __str__(self):
        main_info = self.product.title + ", " + self.product.url
        if self.all_pass:
            main_info = main_info + "检查通过"
            return
        else:
            if self.title_result:
                main_info = main_info + ",标题："+str(self.title_result)
            if self.head_result:
                main_info = main_info + ",购买信息:"+str(self.head_result)
            if self.content_result:
                main_info = main_info + ",详情:"+str(self.content_result)
            if self.image_result:
                main_info = main_info + ",图片:" + str(self.image_result)

        return main_info
