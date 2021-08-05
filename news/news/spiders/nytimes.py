import scrapy
from ..items import Article


class NytimesSpider(scrapy.Spider):
    name = 'nytimes'
    allowed_domains = ['www.nytimes.com']
    start_urls = ['http://www.nytimes.com/']

    def parse(self, response):
        for url in response.css('a::attr(href)').getall():
            if 'nytimes' not in url:
                url = 'http://www.nytimes.com/' + url

            if '/2021/08/05/' in url and '/interactive/' not in url and \
                '/live/' not in url and '/slideshow/' not in url:
                yield scrapy.Request(url, callback=self.parse_article)
            elif '/section/' in url: 
                yield scrapy.Request(url, callback=self.parse)

    def parse_article(self, response):
        item = Article()

        item['title'] = response.css('h1::text').get()
        item['author'] = response.css('span[itemprop=name] a::text').getall()

        if item['author'] == []:
            item['author'] = response.css('span[itemprop=name]::text').getall()

        item['date'] = response.css('time::attr(datetime)').get()
        item['url'] = response.url

        return item