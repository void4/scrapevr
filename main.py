#scrapy runspider main.py -o out.json
import scrapy
import os
import re

# Returns all content within a comment
regex = re.compile(r'<!--(.*)-->', re.DOTALL)

# Remove the output file, as scrapy appends by default
os.system("rm out.json")

# These URLs are not crawled, as they generate dynamic content
forbidden = ["usagii.net", "thevirtualarts.com/JanusVR/streetview.php", "spyduck.net/gridcity/"]

class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    start_urls = ['http://www.janusvr.com/newlobby/index.html']

    def parse(self, response):

        # Add all <Link> url attributes that are not within comments
        urls = [response.urljoin(url) for url in response.css("Link::attr(url)").extract()]

        # Add all <Link> url attributes within comments
        for comment in response.xpath('//comment()').re(regex):
            sel = scrapy.Selector(text=comment, type="html")
            urls += [response.urljoin(url) for url in sel.css("Link::attr(url)").extract()]

        # Return the current page node
        yield {'url':response.url, 'title': response.css('title::text').extract_first(), 'linksto':urls}

        # Branch out to all linked URLs
        for url in urls:
            if any(fbd in url for fbd in forbidden):
                return

            yield scrapy.Request(url, callback=self.parse)
