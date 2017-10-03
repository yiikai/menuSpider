# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import scrapy

class Menu_resource_title_download(FilesPipeline):
	def get_media_requests(self,item,info):
		titleimg = item['title']['imgpath']
		if titleimg is not None:
			yield scrapy.Request(titleimg)

	def item_completed(self, results, item, info):
       		image_path = [ x['path'] for ret,x in results if ret ]
		item['title']['imgpath'] = image_path
        	return item

class Menu_resource_setp_download(FilesPipeline):
	def get_media_requests(self,item,info):
		steps = item['steps']
		for i in steps:
			if i['imgpath'] is not None:
				yield scrapy.Request(i['imgpath'])
	
	def item_complete(self,results,item,info):
		steps = item['steps']
       		image_path = [ x['path'] for ret,x in results if ret ]
		

from DBhandler.mysqlhandler import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MenuPipeline(object):
    def process_item(self, item, spider):
	title = item['title']
	ingredient = item['ingredient'] #dict list
	ingredient = json.dumps(ingredient)
	steps = item['steps']		#dict list
	steps = json.dumps(steps)
	tmptitle = title['name'].encode('utf-8').strip()
	print "======"
	dbitem = Menu(title=tmptitle,title_img=title['imgpath'][0].encode('utf-8'),ingredient=ingredient.encode('utf-8'),steps=steps.encode('utf-8'))
	dbhandler = mysqlhandler("Menu","127.0.0.1","root")
	dbhandler.add_item(dbitem)
	dbhandler.disconnect()	
        return DropItem(item)
