from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import os
import dotenv

from gb_parse.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    login = os.getenv("USERNAME")
    password = os.getenv("ENC_PASSWORD")
    crawler_proc.crawl(
        InstagramSpider,
        login=os.getenv("USERNAME"),
        password=os.getenv("ENC_PASSWORD"),
        tags=["python", "programming"],
    )
    crawler_proc.start()
