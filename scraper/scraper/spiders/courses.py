# -*- coding: utf-8 -*-

from datetime import datetime
import re
import scrapy


class CoursesSpider(scrapy.Spider):
    name = "courses"

    start_urls = [
        'https://www.thw-ausbildungszentrum.de/THW-BuS/DE/Ausbildungsangebot/Lehrgangskalender/lehrgangskalender_node.html'
    ]

    def parse(self, response):
        COURSE_SELECTOR = 'div.course'
        NEXT_PAGE_SELECTOR = 'li.forward a.forward::attr(href)'
        LAST_MINUTE_SEATS_EXPRESSION = r'^Noch (?P<num_seats>\d+) Last-Minute-Plätze verfügbar$'

        for course in response.css(COURSE_SELECTOR):
            def extract_with_css(query):
                return course.css(query).get(default='').strip()

            def get_last_minute_seats(sentence):
                match = re.search(LAST_MINUTE_SEATS_EXPRESSION, sentence)

                if match is not None:
                    return int(match.group('num_seats'))

            yield {
                'course_number': extract_with_css('span.metadata::text'),
                'complete_name': extract_with_css('h2 > a::text'),
                'start': extract_with_css('dl.docData dd:first-of-type::text'),
                'end': extract_with_css('dl.docData dd:last-of-type::text'),
                'registration_period': extract_with_css('dl.courseAction dd::text') or None,
                'last_minute_seats': get_last_minute_seats(extract_with_css('p.courseAction a::text')),
                'scraped_ts': datetime.now().timestamp(),
            }

        # next_page = response.css(NEXT_PAGE_SELECTOR).get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
