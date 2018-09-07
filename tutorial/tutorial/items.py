import scrapy
from scrapy.loader.processors import TakeFirst, Join


class Item(scrapy.Item):
    retailer_sku = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    retailer = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    gender = scrapy.Field(output_processor=TakeFirst())
    sub_category = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field()
    description = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    skus = scrapy.Field(output_processor=Join())
