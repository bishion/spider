from urllib import request, parse
import json, re
from conf.white_list_conf import white_list_service


class JixianciCheck(object):

    @staticmethod
    def checkContent(content):
        if not content:
            return None
        url = "http://ezxcom.com/gn/jixianci/so.php"
        post_data = {
            "val": white_list_service.filter_white_list(content),
            "type": "so"
        }
        data = bytes(parse.urlencode(post_data), encoding="utf-8")
        response = request.urlopen(url, data=data)
        result_json = response.read().decode('unicode_escape').replace("\\", "")
        if not str.endswith(result_json, '"0"}'):
            result_obj = json.loads(result_json, encoding="utf-8", strict=False)
            return re.findall('<span>(.*?)</span>', result_obj["code"], re.S)
        return None


if __name__ == '__main__':
    result = JixianciCheck.checkContent("你好最好的郭芳碧最佳")
    print("极限词", result)
