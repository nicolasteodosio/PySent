# -*- coding: utf-8 -*-
import os

import scrapy
from unidecode import unidecode


class GooglePlaySpider(scrapy.Spider):
    name = 'googleplay_spider'
    start_urls = ['https://play.google.com/store/apps/details?id=com.snapchat.android']

    def parse(self, response):
        coments = response.selector.xpath("//div[@class='review-text']/text()").extract()
        stars = response.selector.xpath("//div[@class='featured-review-star-rating']"
                                          "/div[@class='tiny-star star-rating-non-editable-container']/@aria-label").extract()
        word_dict = dict(zip(coments, stars))
        # with open(os.path.abspath('tt.txt'),  'wb') as f:
        #         for x in coments:
        #             if x != u' ':
        #                 f.write(unidecode(x) + '\n')
