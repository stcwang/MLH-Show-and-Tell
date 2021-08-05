import scrapy
from scrapy.spiders import SitemapSpider
from ..items import Article


class Nytimes3Spider(SitemapSpider):
    name = 'nytimes3'
    allowed_domains = ['www.nytimes.com']
    sitemap_urls = ['https://www.nytimes.com/sitemaps/new/sitemap-2021-08.xml.gz']
    # sitemap_rules = [('/2021/08/05/', 'parse')]

    def sitemap_filter(self, entries):
        for entry in entries:
            if '/2021/08/05/' in entry['loc'] and '/interactive/' not in entry['loc'] and \
                '/live/' not in entry['loc'] and '/slideshow/' not in entry['loc']:
                yield entry

    def parse(self, response):
        item = Article()

        item['title'] = response.css('h1::text').get()
        item['author'] = response.css('span[itemprop=name] a::text').getall()

        if item['author'] == []:
            item['author'] = response.css('span[itemprop=name]::text').getall()

        item['date'] = response.css('time::attr(datetime)').get()
        item['url'] = response.url

        return item