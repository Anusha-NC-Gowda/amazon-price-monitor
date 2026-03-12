import scrapy

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.in"]

    start_urls = [
        "https://www.amazon.in/s?k=skf+bearing"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):

        products = response.css("div.s-result-item")

        for product in products:

            asin = product.attrib.get("data-asin")
            title = product.css("h2 span::text").get()
            price = product.css("span.a-price-whole::text").get()
            rating = product.css("span.a-icon-alt::text").get()
            reviews = product.css("span.a-size-base::text").get()
            link = product.css("h2 a::attr(href)").get()

            if asin and title:
                yield {
                    "ASIN": asin,
                    "Title": title.strip(),
                    "Price": price,
                    "Rating": rating,
                    "Reviews": reviews,
                    "Product_Link": response.urljoin(link)
                }