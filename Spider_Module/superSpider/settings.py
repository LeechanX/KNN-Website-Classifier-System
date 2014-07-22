# Scrapy settings for superSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'superSpider'
ITEM_PIPELINES = {
	'superSpider.pipelines.SuperspiderPipeline':1,
	}
SPIDER_MODULES = ['superSpider.spiders']
NEWSPIDER_MODULE = 'superSpider.spiders'
DOWNLOAD_TIMEOUT=10
CONCURRENT_REQUESTS=32