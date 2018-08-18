# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from maoyan.items import MaoyanItem


class Getmaoyantop100Spider(CrawlSpider):
    name = 'getMaoyanTop100'
    allowed_domains = ['www.maoyan.com']
    start_urls = ['http://www.maoyan.com/board/4']

    rules = [Rule(LinkExtractor(allow=(r'board/4(\?offset=\d+)')), callback="get_parse", follow=True)]

    def get_parse(self, response):
        movie_list = response.xpath('//*[@id="app"]/div/div/div[1]/dl/dd')

        for movie in movie_list:
            sort = movie.xpath('./i/text()').extract()[0].strip()
            title = movie.xpath('./a/@title').extract()[0].strip()
            actor = movie.xpath('./div/div/div[1]/p[2]/text()').extract()[0].strip()
            releasetime = movie.xpath('./div/div/div[1]/p[3]/text()').extract()[0].strip()
            integer = movie.xpath("./div/div/div[2]/p/i[1]/text()").extract()[0].strip()
            fraction = movie.xpath("./div/div/div[2]/p/i[2]/text()").extract()[0].strip()

            print(sort, title, actor, releasetime, integer, fraction)
            item = MaoyanItem()

            item['sort'] = sort
            item['name'] = title
            item['actor'] = actor
            item['releasetime'] = releasetime
            item['score'] = integer+fraction

            yield item
