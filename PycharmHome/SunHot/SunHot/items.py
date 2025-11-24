# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SunhotItem(scrapy.Item):
    # define the fields for your item here like:
    #每个帖子的标题
    title=scrapy.Field()
    #每个帖子的编号
    numbers=scrapy.Field()
    # name = scrapy.Field()
    pass
