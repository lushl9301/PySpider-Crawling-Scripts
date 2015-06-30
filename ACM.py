#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-06-29 15:28:33
# Project: ACM
# Author: Lu Shengliang

import re
from libs.base_handler import *

class Handler(BaseHandler):
    '''
    this is a sample handler
    '''
    crawl_config = {
        "headers": {
            "User-Agent": "BaiDu_Spider",
        }
    }
    
    def on_start(self):
        self.crawl('http://dl.acm.org/citation.cfm?id=1571941.1572041&coll=DL&dl=GUIDE&CFID=514335100&CFTOKEN=57665532',
                   callback=self.detail_page)
        self.crawl('http://dl.acm.org/results.cfm?h=1&cfid=514335100&cftoken=57665532',
                   age=0, callback=self.index_page)
        
    def index_page(self, response):
        for each in response.doc('a').items():
            if re.match('http://dl\.acm\.org\/citation\.cfm\?id=.+CFTOKEN.+', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
            if re.match('http://dl\.acm\.org\/results\.cfm\?query=.+$', each.attr.href):
                self.crawl(each.attr.href, callback=self.index_page)
        
    @config(fetch_type="js")
    def detail_page(self, response):
        self.index_page(response) #bug here, cannot grap table of contents from detail page
        #self.crawl(response.doc('#text12').attr.href, callback=self.index_page)
        
        return {
                "url": response.url,
                "title": response.doc('#divmain > div').text(),
                #"authors": [x.text() for x in response.doc('.authorName').items()],
                "abstract": response.doc('#abstract').text(),
                }