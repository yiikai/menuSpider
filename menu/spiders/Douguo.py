#coding=utf-8
import scrapy
import sys
from scrapy.loader import  ItemLoader
from scrapy import Item
from menu.items import MenuItem
import logging

reload(sys)
sys.setdefaultencoding( "utf-8" )

#豆果美食的爬虫
class DouguoSpider(scrapy.Spider):
    name = 'Douguo'
    root_url = 'http://www.douguo.com'
    init_url = ['http://www.douguo.com/caipu','http://www.douguo.com/caipu/%E6%97%A5%E6%9C%AC%E6%96%99%E7%90%86',]#['http://www.douguo.com/shicai',]
    #菜谱的分类url,从分类的url中在获取出烘焙类的所有的url
    type_url = ['http://www.douguo.com/caipu/fenlei',]
    classify_dict = {}   #食材种类地址分类

    def start_requests(self):
        for url in self.init_url:
            yield scrapy.Request(url,self.every_day_best)
	#详细分类的食谱爬取
	for url in self.type_url:
	    yield scrapy.Request(url,self.cooking_type)

    def cooking_type(self,response):
	#目前只获取烘焙的菜谱
	bakery_type_list = response.css('#ddd13 > ul.kbi >li')
	typedsturl = []
	for i in bakery_type_list:
		url = i.css('a::attr(href)').extract_first()
		if url is not None:
			typedsturl.append(url)
	if typedsturl:
		for i in typedsturl:
			yield scrapy.Request(i,self.every_day_best)
	yield {}		
		


    #every_day_bset 都过所有的类别页面都可以用
    def every_day_best(self,response):
        items_contain = response.css('#container > div.cp_box')
        for item in items_contain:
            url = item.css('div > a.cp_name::attr(href)').extract_first()
            yield scrapy.Request(url,self.detail_item_parser)

	next_page = response.css('#main > div.pagediv.mbm > div > div > div > div > span')
	if len(next_page) == 0:
		next_page = response.css('#main > div.pagediv.mb35 > div > div > div > div > span')
		
        for i in next_page:
            page_name = i.css('span > a::text').extract_first()
            if page_name == u'下一页':
                next_url = i.css('span > a::attr(href)').extract_first()
                yield scrapy.Request(next_url,self.every_day_best)
        yield {}

    def orignal_classify_parser(self,response):
        classify_css = response.css('#main > div.caicont > div.caiputo2')
        for item in classify_css:
            name = item.css('h2::text').extract_first()
            url = item.css('h2 > a::attr(href)').extract_first()
            self.classify_dict[name] = self.root_url + url
            logging.info(self.classify_dict[name])
            yield scrapy.Request(self.classify_dict[name],self.detail_classify_parser)

    def detail_classify_parser(self,response):
        pass

    def detail_item_parser(self,response):
        detailItem = MenuItem()
        title_img = response.css('#main > div.releft > div.recinfo > div.bokpic > div > a::attr(href)').extract_first()
        title_name = response.css('#page_cm_id::text').extract_first()
	title_item = {'name':title_name,"imgpath":title_img,}
        detailItem['title'] = title_item

        ingredient = response.css('#main > div.releft > div.recinfo > div.retew.r3.pb25.mb20 > table > tr:nth-child(n+2)')
        ingredient_list = []
        for i in ingredient:
	    child = i.css('td')
	    for j in child:
		in_name = j.css('span > a::text').extract_first()
		if in_name == None:
			in_name = j.css('span > label::text').extract_first()
            	in_count = j.css('span.right::text').extract_first()
		if in_name == None or in_count == None:
			continue
		ingre_item = {'name':in_name.encode('utf-8'),'count':in_count.encode('utf-8'),}
            	ingredient_list.append(ingre_item)

        detailItem['ingredient'] = ingredient_list

        steps_list = []
        steps = response.css('#main > div.releft > div.recinfo > div.retew.r3.pb25.mb20 > div.step.clearfix')
        steps = steps.css('div.stepcont')
	print len(steps)
        for i in steps:
            img = i.css('div > a::attr(href)').extract_first()
            describe = i.css('p::text').extract_first()
	    if img is  None or describe is None:
		continue
	    step_item = {'step':describe.encode('utf-8'),'imgpath':img.encode('utf-8'),}
            steps_list.append(step_item)
        detailItem['steps'] = steps_list
	detailItem['itemfrom'] = 'douguo'
        return detailItem






