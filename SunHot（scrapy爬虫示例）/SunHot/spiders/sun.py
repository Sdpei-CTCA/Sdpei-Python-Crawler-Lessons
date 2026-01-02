import scrapy

from SunHot.items import SunhotItem
class SunSpider(scrapy.Spider):
    name = "sun"
    allowed_domains = ["wz.sun0769.com"]
    start_urls = ["https://wz.sun0769.com/political/index/politicsNewest?id=1"]

    def parse(self, response):
        items = []
        for each in response.xpath("//li[@class='clear']"):
            item = SunhotItem()
            number = each.xpath('.//span[@class="state1"]/text()').get()
            title = each.xpath('.//span[@class="state3"]/a/text()').get()
            if number and title:  # 确保字段不为空
                item['numbers'] = number
                item['title'] = title
                items.append(item)
        return items
