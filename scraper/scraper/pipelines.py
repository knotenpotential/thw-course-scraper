# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import logging
import requests

class JsonPostPipeline(object):
    def __init__(self, url, api_key):
        self.items = []
        self.url = url
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=crawler.settings.get('JSON_POST_URL'),
            api_key=crawler.settings.get('JSON_POST_API_KEY')
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        headers = {
            'content-type': 'application/json',
            'x-api-key': self.api_key
        }

        data = json.dumps(self.items, ensure_ascii=False).encode('utf-8')
        r = requests.post(self.url, data=data, headers=headers)

        logging.debug(r.status_code)
        r.raise_for_status()
        logging.debug(r.json())

    def process_item(self, item, spider):
        self.items.append(item)
        return item
