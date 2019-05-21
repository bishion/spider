import configparser, os


class WhiteListService(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + "/white_list.ini", encoding="utf-8")
        self.white_list = config.get("common", "white_list")

    def filter_white_list(self, content):
        for word in self.white_list.split(","):
            content = content.replace(word, "")
        return content


white_list_service = WhiteListService()
