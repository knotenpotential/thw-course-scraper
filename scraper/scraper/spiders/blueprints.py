import scrapy


class BlueprintsSpider(scrapy.Spider):
    name = "blueprints"

    start_urls = ['https://www.thw-ausbildungszentrum.de/THW-BuS/DE/Ausbildungsangebot/Lehrgangskatalog/lehrgangskatalog_node.html']

    def parse(self, response):
        BLUEPRINT_SELECTOR = 'table.courses > tbody > tr > td:last-child > a::attr(href)'
        NEXT_PAGE_SELECTOR = 'li a.forward::attr(href)'

        for href in response.css(BLUEPRINT_SELECTOR):
            yield response.follow(href, self.parse_blueprint)

        for href in response.css(NEXT_PAGE_SELECTOR):
            yield response.follow(href, self.parse)

    def parse_blueprint(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'short_name': extract_with_css('div#main span.metadata::text'),
            'long_name': extract_with_css('div#main h1.isFirstInSlot::text'),
            'complete_name': extract_with_css('div#main h1.isFirstInSlot + h2 + p::text'),
        }
