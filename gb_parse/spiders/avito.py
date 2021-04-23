import scrapy

from gb_parse.loaders import AvitoLoader


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = ["https://www.avito.ru/krasnodar/kvartiry/prodam-"]

    _xpath_selectors = {
        "place": "//div[@data-marker='catalog-serp']/div[@data-marker='item']//a[@data-marker='item-title']/@href",
        "pagination": "//div[contains(@class,'pagination-pages')]/a/@href",
    }

    _xpath_data_query = {
        "title": "//h1[@class='title-info-title']/span[@class='title-info-title-text']/text()",
        "url": "//link[@rel='alternate' and @ media]/@href",
        "price": "//div[@class='item-price-wrapper']//span[@class='js-item-price']/text()",
        "address": "//div[@class='item-address']//text()",
        "size": "//div[@class='item-view-block']//span[contains(text(), 'Общая площадь')]//text()",
        "author": "//div[contains(@class,'seller-info-name')]/a/@href",
    }

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow_xpath(
            response, self._xpath_selectors["pagination"], self.parse
        )
        yield from self._get_follow_xpath(
            response, self._xpath_selectors["place"], self.place_parse
        )

    def place_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, selector in self._xpath_data_query.items():
            loader.add_xpath(key, selector)
        #            a = loader.get_output_value(key)
        yield loader.load_item()
