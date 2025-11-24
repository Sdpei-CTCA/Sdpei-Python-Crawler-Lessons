import scrapy
from PycharmHome.items import PycharmhomeItem

class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itheima.com"]
    start_urls = ["https://www.itheima.com/teacher.html"]

    def parse(self, response):
        with open("teacher.html","w",encoding="utf-8") as file:
            file.write(response.text)
        pass
