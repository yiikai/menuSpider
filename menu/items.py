# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MenuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemfrom = scrapy.Field()
    title = scrapy.Field()    #title 包括标题图和名字的元组
    title_img_path = scrapy.Field()
    ingredient = scrapy.Field()  #成份含量元组List
    steps = scrapy.Field()   #steps 包括文字图片的tuple dict
   
