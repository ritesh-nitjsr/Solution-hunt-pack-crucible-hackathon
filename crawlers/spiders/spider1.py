# -*- coding: utf-8 -*-
import scrapy
import re


class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    base_url = "http://www.tatainnoverse.com/"
    start_urls = ['http://www.tatainnoverse.com/index.php//']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.MongoPipeline': 300,
            }
        }

    def parse(self, response):
        for challenge_link in  response.css("section#openchallenges div.content h3 a::attr(href)").extract():
            #yield { (challenge_link.split("="))[1] : challenge_link}
            yield scrapy.Request(self.base_url+challenge_link, callback = self.parse_desc)
    def parse_desc(self, response):
        description = response.xpath(".//*[@id='singlechallengedesc']").xpath("string()").extract()
        title = response.css("div.container h1::text").extract_first()
        desc = description[0]
        desc = desc.replace("\n", " ")
        desc = desc.replace("\t", "")
        desc = desc.replace("\r", "")
        desc = desc.lstrip()
        desc = desc.rstrip()
        desc = re.sub(r'[\(\[].*?[\)\]]', "", desc)
        desc = desc.replace("[", "")
        desc = desc.replace("]", "")
        desc = desc.replace("(", "")
        desc = desc.replace(")", "")
        desc = re.sub(r'\\[a-z, 0-9]*', "", desc)
        desc = re.sub(r'[0-9]*', "", desc)
        desc = re.sub(r'http[a-z,:,/,.,-]*', "",  desc)
        res = {}
    	res["_id"] = (response.url.split("="))[1]
    	res["content"] = desc
        res["title"] = title
        yield res