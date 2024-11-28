import scrapy
import time
import csv
class QuotesSpider(scrapy.Spider):
    name = "mobile"

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        # Initialize lists to store data across multiple pages
        self.titles = []
        self.prices = []
        self.ratings = []
        self.desc = []

    def start_requests(self):
        base_url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page="
        total_pages = 41  # Adjust this based on the number of pages you want to scrape
        
        for page_num in range(1, total_pages + 1):
            url = f"{base_url}{page_num}"
            yield scrapy.Request(url=url, callback=self.parse)
            time.sleep(2)

    def parse(self, response):
        for item in response.css('.tUxRFH'):
            title = item.css('.KzDlHZ::text').get()
            self.titles.append(title)

            price = item.css('.Nx9bqj._4b5DiR::text').get()
            self.prices.append(price)

            rate = item.css('.XQDdHH::text').get()
            self.ratings.append(rate)

            de = item.xpath('.//ul[contains(@class, "G4BRas")]/li/text()').getall()
            self.desc.append(de)
            print(len(self.titles))
            print(len(self.ratings))
            print(len(self.prices))
            print(len(self.desc))

        # Optionally, after scraping all pages, you can yield the data at the end
        # This will run after all pages are scraped
        if response.status == 200 and response.url.endswith('page=400'):
            yield {
                # 'titles': self.titles,
                # 'prices': self.prices,
                # 'ratings': self.ratings,
                # 'desc': self.desc,
            }
        import csv

    def closed(self, reason):
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Rating', 'Description'])
            for i in range(len(self.titles)):
                writer.writerow([
                    self.titles[i],
                    self.prices[i],
                    self.ratings[i],
                    ', '.join(self.desc[i])  # Join description list with a separator
                ])

