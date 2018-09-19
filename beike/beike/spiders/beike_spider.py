# -*- coding: utf-8 -*-
import scrapy
import re
from beike.items import BeikeItem
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
from time import sleep
class BeikeSpiderSpider(scrapy.Spider):
    name = 'beike_spider'
    allowed_domains = ['ke.com']
    start_urls = ['https://www.ke.com/city/']



    def parse(self, response):
        p_divs = response.xpath("//div[@class='city_list_section']/ul/li//div[@class='city_province']")
        for p_div in p_divs:
            province = p_div.xpath("./div[1]/text()").get()
            province = re.sub(r"\s", "", province)
            city_links = p_div.xpath("./ul/li/a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                url_module = city_url.split('.', 1)
                city_part = url_module[0]
                domain_part = url_module[1]
                yield scrapy.Request(url=response.urljoin(city_url), callback=self.parse_zu, meta={'info': (province, city, city_part, domain_part)})


    def parse_zu(self, response):
        province, city, city_part, domain_part = response.meta.get("info")
        zu = response.xpath("//ul/li[@class='CLICKDATA'][3]/a/text()").get()
        if zu == '租房':
            print(city+"有租房业务")
            new_url = "https:"+city_part+".zu."+domain_part+"/zufang/rt200600000001"
            yield scrapy.Request(url=new_url, callback=self.parse_zhengzu,
                                 meta={'info': (province, city, city_part)})
        else:
            print(city+"无租房业务")



    def parse_zhengzu(self,response):
        province, city, city_part = response.meta.get("info")
        divs = response.xpath("//div[@class='content__article']//div[@class='content__list']/div")
        for div in divs:
            name = div.xpath(".//div/p[1]/a/text()").get()
            if name:
                name = re.sub("\s", "", name)
                info_list = div.xpath("./div/p[2]/text()").getall()
                info_list = list(map(lambda x: re.sub("\s", "", x), info_list))
                area = "".join(list(filter(lambda x: x.endswith("㎡"), info_list)))
                rooms = "".join(list(filter(lambda x: x.endswith("卫"), info_list)))
                price = "".join(div.xpath("./div/span//text()").getall())
                time = div.xpath("./div/p[4]/text()").get()
                origin_url = div.xpath("./a[1]/@href").get()
                origin_url = "https:"+city_part+".zu.ke.com"+origin_url
                item = BeikeItem(
                province=province,
                city=city,
                name=name,
                area=area,
                rooms=rooms,
                price=price,
                time=time,
                origin_url=origin_url
                )
                yield item

        driver = webdriver.PhantomJS()
        driver.get(response.url)
        sleep(5)
        # elem = WebDriverWait(driver=driver, timeout=20).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[@class='next']"))
        # )
        # print(elem)
        # driver.implicitly_wait(20)
        source = driver.page_source
        print(source)
        html = etree.HTML(source)
        print(html)
        next_url = html.xpath("//a[@class='next']/@href")[0]
        print(next_url)
        driver.quit()
        if next_url:
            p
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_zhengzu,
                                 meta={'info': (province, city, city_part)})













