import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Article


class Nytimes2Spider(CrawlSpider):
    name = 'nytimes2'
    allowed_domains = ['www.nytimes.com']
    start_urls = ['http://www.nytimes.com/']

    rules = (
        Rule(LinkExtractor(allow='/section/')),
        Rule(LinkExtractor(allow='/2021/08/05/', deny=('/interactive/', '/live/', '/slideshow/')), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        item = Article()

        item['title'] = response.css('h1::text').get()
        item['author'] = response.css('span[itemprop=name] a::text').getall()

        if item['author'] == []:
            item['author'] = response.css('span[itemprop=name]::text').getall()

        item['date'] = response.css('time::attr(datetime)').get()
        item['url'] = response.url

        return item
