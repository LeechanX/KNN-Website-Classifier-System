# -*- coding: utf-8 -*-

import chardet
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy import log

class SuperSpider(CrawlSpider):
    name = 'superspider'
    def __init__(self, start_url,output_file, *args, **kwargs):
        super(SuperSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.start_urls.append(start_url)
        self.output_file=output_file
    def parse(self, response):
        self.parse_detail(response)
    
    def parse_detail(self, response):
        outputfile = self.output_file
        if not outputfile:
            log.msg("download %s fail" % response.url, level = log.WARNING, spider = self)
            return
        content_type=chardet.detect(response.body)
        hxs=HtmlXPathSelector(response)
        maindoing=''
        try:
            if content_type['encoding'] in ['ISO-8859-2','GB2312']:content_type['encoding']='gbk'
            maindoing=response.body.decode(content_type['encoding'])
        except Exception, e:
            maindoing=hxs.extract()
        with open(outputfile, 'w') as f:
            f.write(maindoing.encode("utf-8"))
        print '!!!!!!!',response.url,'!!!!!!!!'
        log.msg("download file: %s" % outputfile, level = log.INFO, spider = self)