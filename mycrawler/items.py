# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, Compose, Join, TakeFirst
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
    to_int = Compose(TakeFirst(), int)

    def parse_story_json_data(json_data):
        return chompjs.parse_js_object(json_data)

    def split_story_authors(story_authors_data):
        return re.split('[,&]+', story_authors_data)

    def sanitize_story_authors(story_authors_data):
        # TODO: check if country is correctly removed
        return re.sub('( aus \w*)', '', story_authors_data)

    def sanitize_posting_count(string_data):
        return re.sub('\W', '', string_data)

    # Story fields
    story_url = Field(output_processor=Compose(lambda s: str(s[0])))
    story_authors = Field(input_processor=MapCompose(
        split_story_authors, sanitize_story_authors, str.strip))
    # TODO: fetch authors from story_content
    # possible regex --> <p>.*\(([^)]+)\)<\/p>
    # story_authors_short = Field()
    story_posting_count = Field(
        input_processor=Compose(lambda s: s[0], sanitize_posting_count), output_processor=Compose(lambda s: int(s[0])))
    story_breadcrumbs = Field()
    story_publication_date = Field(input_processor=Compose(
        lambda s: s[0], str.strip), output_processor=Compose(lambda s: str(s[0])))
    story_modification_date = Field(input_processor=Compose(
        lambda s: s[0], str.strip), output_processor=Compose(lambda s: str(s[0])))
    story_json_data = Field(input_processor=MapCompose(parse_story_json_data))
    story_kicker = Field(output_processor=Compose(lambda s: str(s[0])))
    story_subtitle = Field(output_processor=Compose(lambda s: str(s[0])))
    story_title = Field(output_processor=Compose(lambda s: str(s[0])))
    story_content = Field()
    story_id = Field(output_processor=Compose(lambda s: int(s[0])))
    # story_id = to_int
    # Crawler metadata
    crawler_name = Field(output_processor=Compose(lambda s: str(s[0])))
    # First crawldate
    store_date = Field(output_processor=Compose(lambda s: float(s[0])))
    # Last date of crawl
    store_modification_date = Field(
        output_processor=Compose(lambda s: float(s[0])))
    # File
    store_file = Field(output_processor=Join())


class PostingItem(Item):
    # TODO: sticky comment/from employee --> https://www.derstandard.at/story/2000122058320/wie-familien-trotz-corona-weihnachten-retten-koennen
    posting_story_id = Field()
    # posting_community_name = Field()
    # posting_url = Field()
    # posting_real_id = Field()
    # posting_organization_id = Field()
    # posting_supporter = Field()
    # posting_verified_id = Field()
    # posting_posting_id = Field()
    # posting_parent_posting_id = Field()
    # posting_community_id = Field()
    # posting_community_profile = Field()
    # posting_postdate = Field()
    # posting_title = Field()
    posting_content = Field()
    # posting_ratings_positive = Field()
    # posting_ratings_negative = Field()
    # posting_follower = Field()
    # store_date = Field()
