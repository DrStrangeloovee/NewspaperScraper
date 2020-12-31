# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from newspapercrawler.items import StoryItem, PostingItem
import json
from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import os
import psycopg2
from scrapy.utils.project import get_project_settings
import logging


logger = logging.getLogger("logger")


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
        self.story_items_file = open(
            "data/storage/derstandard/items/story_items.jsonl", "w"
        )
        self.posting_items_file = open(
            "data/storage/derstandard/items/posting_items.jsonl", "w"
        )

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


class DatabasePipeline(object):
    def open_spider(self, spider):
        database_settings = get_project_settings().getdict("DB_SETTINGS")
        logger.info("Database settings %s", database_settings)

    # def close_spider(self, spider):
    #     self.story_items_file.close()
    #     self.posting_items_file.close()

    # def process_item(self, item, spider):
    #     database_settings = SETTINGS.getdict()
    #     logger.info("Database settings %s", database_settings)


# NEW
# class DatabasePipeline(object):
#     # https://stackoverflow.com/questions/14075941/how-to-access-scrapy-settings-from-item-pipeline
#     def __init__(self, db_url, db_user, db_password, db_name, db_port):
#         try:
#             # Connect to the db using options set in settings.py
#             # TODO: add sslmode='require' to connection
#             # self.db_connection = psycopg2.connect(self.db_url, sslmode="require")
#             self.db_connection = psycopg2.connect(
#                 "dbname="
#                 + db_name
#                 + " user="
#                 + db_user
#                 + " host="
#                 + db_url
#                 + " port="
#                 + db_port
#                 + " password="
#                 + db_password
#             )
#         except psycopg2.DatabaseError as e:
#             print(e)
#             exit(42)
#         self.db_connection.autocommit = True
#         self.db_cursor = self.db_connection.cursor()

#     @classmethod
#     def from_crawler(cls, crawler):
#         """Get data base options from settings.py"""
#         db_settings = get_project_settings()
#         # TODO: handle exception
#         # if not db_settings:
#         #     raise NotConfigured
#         return cls(
#             db_url=db_settings.get("DB_URL"),
#             db_user=db_settings.get("DB_USER"),
#             db_password=db_settings.get("DB_PASSWORD"),
#             db_name=db_settings.get("DB_NAME"),
#             db_port=db_settings.get("DB_PORT"),
#         )


# OLD
# class DatabasePipeline(object):
#     """Initialize the data base"""

#     # Fetch settings from settings.py
#     # https://stackoverflow.com/questions/61315923/instantiate-database-connection-in-scrapy-middleware-and-access-it-in-other-modu

#     def __init__(self, db_url, db_user, db_password, db_name, db_port):
#         try:
#             # Connect to the db using options set in settings.py
#             # TODO: add sslmode='require' to connection
#             # self.db_connection = psycopg2.connect(self.db_url, sslmode="require")
#             self.db_connection = psycopg2.connect(
#                 "dbname="
#                 + db_name
#                 + " user="
#                 + db_user
#                 + " host="
#                 + db_url
#                 + " port="
#                 + db_port
#                 + " password="
#                 + db_password
#             )
#         except psycopg2.DatabaseError as e:
#             print(e)
#             exit(42)
#         self.db_connection.autocommit = True
#         self.db_cursor = self.db_connection.cursor()

#     @classmethod
#     def from_crawler(cls, crawler):
#         """Get data base options from settings.py"""
#         db_settings = crawler.settings.getdict("DB_SETTINGS")
#         # TODO: handle exception
#         # if not db_settings:
#         #     raise NotConfigured
#         return cls(
#             db_url=db_settings.get("DB_URL"),
#             db_user=db_settings.get("DB_USER"),
#             db_password=db_settings.get("DB_PASSWORD"),
#             db_name=db_settings.get("DB_NAME"),
#             db_port=db_settings.get("DB_PORT"),
#         )

#     def open_spider(self, spider):
#         """Initialize table when spider opens"""
#         self.db_table_name = spider.name
#         # Create a table with the same name as the spider if it does not exist already
#         self.db_cursor.execute(
#             "CREATE TABLE IF NOT EXISTS "
#             + self.db_table_name
#             + " (url text PRIMARY KEY, visited timestamp, published timestamp, title text, description text, text text, author text[], keywords text[]);"
#         )

#     def close_spider(self, spider):
#         """Close the connection when spider closes"""
#         self.db_connection.commit()
#         self.db_connection.close()

#     def process_item(self, item, spider):
#         """Process items and insert into data base"""
#         try:
#             # Needs postgresql version >= 9.5 for UPSERT, else remove "ON CONFLICT ..." line and handle duplicates
#             self.db_cursor.execute(
#                 "INSERT INTO "
#                 + self.db_table_name
#                 + " "
#                 + "VALUES (%s, %s, %s ,%s ,%s, %s, %s, %s) "
#                 + "ON CONFLICT DO NOTHING ;",
#                 (
#                     item["url"],
#                     item["visited"],
#                     item["published"],
#                     item["title"],
#                     item["description"],
#                     item["text"],
#                     item["author"],
#                     item["keywords"],
#                 ),
#             )
#         except psycopg2.DatabaseError as e:
#             print(e)
#         return item