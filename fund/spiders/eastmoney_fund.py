# -*- coding: utf-8 -*-
import execjs
import scrapy

from fund.items import EastmoneyFundItem


class EastmoneyFundSpider(scrapy.Spider):
    name = 'eastmoney_fund'
    allowed_domains = ['eastmoney.com']

    def start_requests(self):
        fund_list_url = "http://fund.eastmoney.com/js/fundcode_search.js"
        yield scrapy.Request(
            url=fund_list_url,
            dont_filter=True,
            meta={"dont_cache": True},
            callback=self.parse,
        )

    def parse(self, response):
        js_content = execjs.compile(response.text)
        name = js_content.eval('r')
        for one in name:
            if "(后端)" not in one[2]:
                item = EastmoneyFundItem(
                    code=one[0],
                    initials=one[1],
                    name=one[2],
                    type=one[3],
                    pinyin=one[4],
                )
                yield item
