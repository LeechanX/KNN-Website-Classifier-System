# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SuperspiderPipeline(object):
	def __init__(self):
		self.filename='shit.txt'
	def close_spider(self,spider):
		print 'Bye'
	def process_item(self,item,spider):
		item['status']=0
		if 'title' in item and item['title']:
			item['status']+=1
			item['title']=item['title'][0]
		if 'keyword' in item and item['keyword']:
			item['status']+=2
			item['keyword']=item['keyword'][0]
		if 'description' in item and item['description']:
			item['status']+=4
			item['description']=item['description'][0]
		if 'content' in item and item['content']:
			item['content']=item['content'][0]
		