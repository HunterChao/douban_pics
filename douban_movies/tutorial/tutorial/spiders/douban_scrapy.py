# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy import Request
from tutorial2.items import Tutorial2Item
import urllib.request
import re
import json

'''
  使用Scrapy抓取豆瓣电影简介，评分、简介信息图片
'''

class doubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ["douban.com"]
    start_list = []
    for i in range(1,14):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=' + str(i*20)
        start_list.append(url)
    start_urls = start_list   # 定义start_urls为一个存储链接的列表

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        hxs = response.body.decode('utf-8')
        # hxs = Selector(text=response.body.decode('utf-8'))    # 这句有问题
        # print(hxs)
        hjson = json.loads(hxs)    # 字典
        for lis in hjson['subjects']:
            item = Tutorial2Item()       # 实例化类
            item["info"] = lis['url']
            item["pic"] = lis['cover']
            item["score"] = lis['rate']
            item["title"] = lis['title']
            filename = item["title"] + '_' + item["score"] + '分' + '.jpg'
            urllib.request.urlretrieve(item["pic"], filename)
            yield item

