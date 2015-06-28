#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-10-31 13:05:52
# Author: https://github.com/binux

# Crawling starts with articles and journals
# Take each page as index page and extract related papers

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
        self.crawl('http://www.sciencedirect.com/science/article/pii/S1568494612005741',
                   callback=self.detail_page)
        self.crawl('http://www.sciencedirect.com/science/article/pii/S0167739X12000581',
                   age=0, callback=self.detail_page)
        self.crawl('http://www.sciencedirect.com/science/journal/09659978',
                   age=0, callback=self.index_page)
        
    def index_page(self, response):
        for each in response.doc('a').items():
            if re.match('http://www.sciencedirect.com/science/article/pii/\w+$', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        
    @config(fetch_type="js")
    def detail_page(self, response):
        self.index_page(response)
        self.crawl(response.doc('#relArtList > li > .cLink').attr.href, callback=self.index_page)
        
        return {
                "url": response.url,
                "title": response.doc('.svTitle').text(),
                "authors": [x.text() for x in response.doc('.authorName').items()],
                "abstract": response.doc('.svAbstract > p').text(),
                "keywords": [x.text() for x in response.doc('.keyword span').items()],
                }
