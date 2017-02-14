#scrapy runspider main.py -o out.json
import scrapy
import os
import re
import random
regex = re.compile(r'<!--(.*)-->', re.DOTALL)

os.system("rm out.json")

# ["usagii.net"]
forbidden = ["thevirtualarts.com/JanusVR/streetview.php", "spyduck.net/gridcity/"]

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.janusvr.com/newlobby/index.html']

    def parse(self, response):
        urls = [response.urljoin(url) for url in response.css("Link::attr(url)").extract()]
        for comment in response.xpath('//comment()').re(regex):
            sel = scrapy.Selector(text=comment, type="html")
            urls += [response.urljoin(url) for url in sel.css("Link::attr(url)").extract()]
        yield {'url':response.url, 'title': response.css('title::text').extract_first(), 'linksto':urls}
        for url in urls:

            if any(fbd in url for fbd in forbidden):
                return

            yield scrapy.Request(url, callback=self.parse)
