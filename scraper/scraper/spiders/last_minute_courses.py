# -*- coding: utf-8 -*-

import arrow
import re
import scrapy


class LastMinuteCoursesSpider(scrapy.Spider):
    name = "last_minute_courses"

    start_urls = [
        'https://www.thw-ausbildungszentrum.de/THW-BuS/DE/Ausbildungsangebot/Lehrgangskalender/lehrgangskalender_node.html?sort=lastMinute'
    ]

    def parse(self, response):
        COURSE_SELECTOR = 'div.course'
        NEXT_PAGE_SELECTOR = 'li.forward a.forward::attr(href)'
        SHORT_NAME_RE = r'^Standort \D+ [-|–] (?P<short_name>[H|N] \d{3}[a-zA-Z]?/\d{2})$'
        LAST_MINUTE_RE = r'^Noch (?P<num_seats>\d+) Last-Minute-Plätze verfügbar$'
        hyperlink_re = re.compile(r'')
        HYPERLINK_RE_REPL = r'\1\3'

        for course in response.css(COURSE_SELECTOR):
            def extract_with_css(query):
                return course.css(query).get(default='').strip()

            def get_short_name(sentence):
                match = re.search(SHORT_NAME_RE, sentence)

                if match is not None:
                    return match.group('short_name')

            def get_last_minute_seats(sentence):
                match = re.search(LAST_MINUTE_RE, sentence)

                if match is not None:
                    return int(match.group('num_seats'))

            def get_hyperlink(sentence):
               return sentence

            if course.css('p.courseAction a::text').get() is not None:
                yield {
                    'short_name': get_short_name(extract_with_css('span.metadata::text')),
                    'num_seats': get_last_minute_seats(extract_with_css('p.courseAction a::text')),
                    'hyperlink': get_hyperlink(extract_with_css('p.courseAction a::attr(href)')),
                    'scraped_ts': arrow.now().isoformat(),
                }
            else:
                return

        next_page = response.css(NEXT_PAGE_SELECTOR).get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
