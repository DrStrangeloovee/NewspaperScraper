# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from dataclasses import dataclass
from scrapy.loader.processors import MapCompose
import chompjs
import re


class MycrawlerItem(Item):
    # Story fields
    test = Field()


class TestItem(Item):
    # Story fields
    story_url = Field()


class StoryItem(Item):
    # TODO: add author shortnames from end of article

    def parse_story_json_data(json_data):
        return chompjs.parse_js_object(json_data)

    def split_story_authors(story_authors_data):
        return re.split('[,&]+', story_authors_data)

    def sanitize_story_authors(story_authors_data):
        # TODO: check if country is correctly removed
        return re.sub('( aus \w*)', '', story_authors_data)

    # Story fields
    story_url = Field()
    story_authors = Field(input_processor=MapCompose(
        split_story_authors, sanitize_story_authors, str.strip))
    # TODO: fetch authors from story_content
    # story_authors_short = Field()
    story_posting_count = Field()
    story_breadcrumbs = Field()
    story_publication_date = Field()
    story_modification_date = Field()
    story_json_data = Field(input_processor=MapCompose(parse_story_json_data))
    story_kicker = Field()
    story_subtitle = Field()
    story_title = Field()
    story_content = Field()
    story_id = Field()
    # Crawler metadata
    crawler_name = Field()
    # First crawldate
    store_date = Field()
    # Last date of crawl
    store_modification_date = Field()
    # File
    store_file = Field()


class CommentItem():
    # TODO: sticky comment/from employee --> https://www.derstandard.at/story/2000122058320/wie-familien-trotz-corona-weihnachten-retten-koennen
    comment_community_name = Field()
    comment_url = Field()
    comment_real_id = Field()
    comment_organization_id = Field()
    comment_supporter = Field()
    comment_verified_id = Field()
    comment_posting_id = Field()
    comment_parent_posting_id = Field()
    comment_community_id = Field()
    comment_community_profile = Field()
    comment_postdate = Field()
    comment_content = Field()
    comment_ratings_positive = Field()
    comment_ratings_negative = Field()
    comment_follower = Field()
    store_date = Field()
