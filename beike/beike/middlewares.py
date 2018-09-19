# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse


class RandomUserAgentDownloaderMiddleware(object):
    USER_AGENTS = [
        'Mozilla/5.0 (X11; CrOS i686 1660.57.0) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.46 Safari/535.19',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.113 Safari/534.30 ',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080414 Firefox/2.0.0.14 Flock/1.1.2',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080326 Firefox/2.0.0.13 Flock/1.1.1',
        'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.8.1.11) Gecko/20080131 Firefox/2.0.0.11 Flock/1.0.8',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051007 Galeon/2.0.0 (Debian package 2.0.0-1)',
        'Mozilla/5.0 (X11; U; Linux i686) Gecko/20030430 Galeon/1.3.4 Debian/1.3.4.20030509-1',
        'Opera/9.01 (X11; OpenBSD i386; U; en)',
        'Opera/9.02 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/525.26.2 (KHTML, like Gecko) Version/3.2 Safari/525.26.13',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB) AppleWebKit/525.19 (KHTML, like Gecko) Version/3.1.2 Safari/525.21'
    ]


    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        user_agent = random.choice(self.USER_AGENTS)
        print(user_agent)
        request.headers['User-Agent'] = user_agent



class RandomProxyDownloaderMiddleware(object):

    PROXIES = [
        {'ip_port': '39.135.10.164:8080', },
        {'ip_port': '180.165.110.9:53281', },
        {'ip_port': '183.129.244.17:31773', },
        {'ip_port': '221.193.222.7:8060', },
        {'ip_port': '59.62.7.247:9000', },
        {'ip_port': '58.211.56.36:47431', },



     ]
    def process_request(self, request, spider):

        proxy = random.choice(self.PROXIES)
        print(proxy)
        # if proxy['user_passwd'] is None:
        request.meta['proxy'] = "http://" + proxy['ip_port']
        # else:
        #     base64_userpasswd = base64.b64encode(proxy['user_passwd'].encode("utf-8"))
        #     request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd.decode("utf-8")
        #     request.meta['proxy'] = "http://" + proxy['ip_port']




