from src.modules.calculate_module.crawler_factory.crawler import Crawler
from src.modules.calculate_module.crawler_factory.xskt_crawler import XSKTCrawler
class CrawlerCreator:
	def __init__(self) -> None:
		pass

	@classmethod
	def create_crawler(self) -> Crawler:
		self.crawler = XSKTCrawler()
		return self.crawler