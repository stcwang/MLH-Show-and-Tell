# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicatePipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        article = ItemAdapter(item)
        tup = (article['title'], article['date'])

        if tup in self.seen:
            raise DropItem(f'Duplicate item: {item}')
        else:
            self.seen.add(tup)
            return item
