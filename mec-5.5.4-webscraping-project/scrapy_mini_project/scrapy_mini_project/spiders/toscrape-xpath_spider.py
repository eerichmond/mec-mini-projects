import scrapy


class ToScrapeXpathSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        url = "http://quotes.toscrape.com/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.xpath("//div[contains(@class, 'quote')]"):
            yield {
                "text": quote.xpath("span[contains(@class, 'text')]/text()").get(),
                "author": quote.xpath("*/small[contains(@class, 'author')]/text()").get(),
            }

        next_page = response.xpath("//li[contains(@class, 'next')]/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
