# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from mycrawler.items import StoryItem, PostingItem
import json
from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class MycrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:

    # def open_spider(self, spider):
    #     self.file = open('data/items/items.json', 'wb')
    #     self.file.write("[")

    # def close_spider(self, spider):
    #     self.file.write("]")
    #     self.file.close()

    # def process_item(self, item, spider):
    #     line = json.dumps(
    #         dict(item),
    #         sort_keys=True,
    #         indent=4,
    #         separators=(',', ': ')
    #     ) + ",\n"

    #     self.file.write(line)
    #     return item

    def open_spider(self, spider):
        self.story_items_file = open("data/items/story_items.jsonl", "w")
        self.posting_items_file = open("data/items/posting_items.jsonl", "w")

    def close_spider(self, spider):
        self.story_items_file.close()
        self.posting_items_file.close()

    def process_item(self, item, spider):
        if isinstance(item, StoryItem):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.story_items_file.write(line)
            return item
        if isinstance(item, PostingItem):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.posting_items_file.write(line)
            return item
