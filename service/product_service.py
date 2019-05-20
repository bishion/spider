from utils.baidu_ocr import BaiduOcr
from utils.jixianci import JixianciCheck
from dto.product import Product
from dto.check_result import CheckResultDTO


class ProductService(object):
    @staticmethod
    def check_product(product: Product):
        title_result = JixianciCheck.checkContent(product.title)
        head_result = JixianciCheck.checkContent(product.head)
        content_result = JixianciCheck.checkContent(product.content)
        image_result = ProductService.check_img_content(product.images)

        return CheckResultDTO(product, title_result, head_result, content_result, image_result)

    @staticmethod
    def check_img_content(img_urls):
        if not img_urls:
            return None
        img_result = {}
        baidu_ocr = BaiduOcr()
        for url in img_urls:
            img_words = baidu_ocr.read_image_words(url)
            if img_words:
                img_check_result = JixianciCheck.checkContent(img_words)
                if img_check_result:
                    img_result[url] = img_check_result

        return None if len(img_result) == 0 else img_result
