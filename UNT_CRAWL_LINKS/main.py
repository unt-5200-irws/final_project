import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from scrapy.linkextractors import LinkExtractor
import os
l=[]
class Untspider(Spider):

    name = 'myUntSpider'
    #start_urls=['https://www.unt.edu/search-results?search=&sa=Search']
    start_urls = ['https://ci.unt.edu/sitemap']
    #start_urls = ['https://www.unt.edu']
    allowed_domains=['unt.edu']
    try:
        os.remove('myuntsavesitemap.txt')
    except OSError:
        pass
    custom_settings = {
        'CONCURRENT_REQUEST' : 2,
        'AUTO_THROTTLE_ENABLED' : True
    }
    def __init__(self):
        self.link_extractor = LinkExtractor(allow="https://www.unt.edu/" , unique = True)
    def parse(self, response):

        for link in self.link_extractor.extract_links(response):
            with open('myuntsavesitemap.txt','a+') as f:
                f.write(f"\n{str(link)}")
                l.append(str(link))
            yield  response.follow(url = link, callback = self.parse )

if __name__ == "__main__" :
    k=[]
    process = CrawlerProcess()
    process.crawl(Untspider)
    process.start()
    print(len(l))
    l.sort()
    print(l)
    s = set(l)
    with open(r'sitemapunique.txt', 'w') as fp:
        for item in s:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')

