from dto.product import Product
class CheckResultDTO(object):
    def __init__(self,product:Product,title_result,head_result,content_result,image_result):
        self.title_result = title_result
        self.head_result = head_result
        self.content_result = content_result
        self.image_result = image_result
        self.product = product

