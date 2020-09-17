import scrapy


class PsacardbotSpider(scrapy.Spider):
    name = 'psacardbot'
    allowed_domains = ['https://www.psacard.com/auctionprices']
    start_urls = ['http://https://www.psacard.com/auctionprices/']

    def parse(self, response):
        pass
