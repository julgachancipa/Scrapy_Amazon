import scrapy
from ..items import ScrapyAmazonItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1601577440&rnid=1250225011&ref=lp_283155_nr_p_n_publication_date_0'
    ]

    def parse(self, response):
        items = ScrapyAmazonItem()

        product_name = response.css('.a-color-base.a-text-normal::text').extract()
        product_author = response.css('.a-color-secondary .a-size-base.a-link-normal::text').extract()
        product_price = response.css('.a-spacing-top-small .a-price:nth-child(1) .a-offscreen::text').extract()
        product_image_link = response.css('.s-image::attr(src)').extract()

        product_author = [p_a.strip(' \n') for p_a in product_author]

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_image_link'] = product_image_link

        yield items

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page=' +\
                    str(AmazonSpider.page_number) + '&fst=as%3Aoff&qid=1601577446&rnid=1250225011&ref=sr_pg_2'

        if AmazonSpider.page_number <= 75:
            AmazonSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
