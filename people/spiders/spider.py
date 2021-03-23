import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import PeopleItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class PeopleSpider(scrapy.Spider):
	name = 'people'
	start_urls = ['https://peoplesbankal.com/blog']

	def parse(self, response):
		post_links = response.xpath('//p[@class="alignright"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="meta"]/p/text()').get().split('on ')[1]
		title = response.xpath('//h2[@class="entry-title"]/text()').get()
		content = response.xpath('//article[@class="post"]//text()[not (ancestor::div[@class="meta"] or ancestor::h2[@class="entry-title"] or ancestor::div[@class="meta"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=PeopleItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
