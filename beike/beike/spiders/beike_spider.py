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
            print('*' * 100)
            print(next_url)
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_zhengzu,
                                 meta={'info': (province, city, city_part)})
            print('*'*100)












# from scrapy.spiders import CrawlSpider, Rule
# from jianshu.items import JianshuItem
#
# class JianshuSpiderSpider(CrawlSpider):
#     name = 'jianshu_spider'
#     allowed_domains = ['jianshu.com']
#     start_urls = ['http://jianshu.com/']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'.*/p/[0-9a-z][12].*'), callback='parse_detail', follow=True),
#     )
#
#     def parse_detail(self, response):
#         title = response.xpath("//h1[@class='title']/text()").get()
#         avatar = response.xpath("heng='avatar']/img/@src").get()
#         author = response.xpath("//span[@class='name']/a/text()").get()
#         pub_time = response.xpath("//span[@class='publish-time']/text()").get().replace("*","")
#         #获取文章id
#         url = response.url
#         url1 = url.split("?")[0]
#         article_id = url1.split("/")[-1]
#         #文章内容，包括标签，而不是存文本内容
#         content = response.xpath("//div[@class='show-content']").get()
#         # word_count = response.xpath("//span[@class='wordage']/text()").get()
#         # comment_count = response.xpath("//span[@class='comments-count']/text()").get()
#         # read_count = response.xpath("//span[@class='views-count']/text()").get()
#         # like_count = response.xpath("//span[@class='likes-count']/text()").get()
#         # subjects = ",".join(response.xpath("//div[@class='include-collection']/a/div/text()").getall())
#
#         item = JianshuItem(
#             title=title,
#             avatar=avatar,
#             pub_time=pub_time,
#             author=author,
#             origin_url=response.url,
#             content=content,
#             article_id=article_id,
#             # subjects=subjects,
#             # word_count=word_count,
#             # comment_count=comment_count,
#             # like_count=like_count,
#             # read_count=read_count
#         )
#         yield item






#selenium
# from selenium import webdriver
# from lxml import etree
# import re
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
# class LagouSpider(object):
#     def __init__(self):
#         self.driver = webdriver.Chrome()
#         #python职位
#         self.url = 'https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput='
#         self.position = []
#
#     def run(self):
#         self.driver.get(self.url)
#         while True:
#             source = self.driver.page_source
#             WebDriverWait(driver=self.driver,timeout=20).until(
#                 EC.presence_of_element_located((By.XPATH,"//div[@class='pager_container']/span[last()]"))
#             )
#             self.parse_list_page(source)
#             #点“下一页”
#             next_btn = self.driver.find_element_by_xpath(
#                 "//div[@class='pager_container']/span[last()]")
#             if "pager_next_disabled" in next_btn.get_attribute("class"):
#                 break
#             else:
#                 next_btn.click()
#             time.sleep(1)
#
#
#     def parse_list_page(self,source):
#         html = etree.HTML(source)
#         links = html.xpath("//a[@class='position_link']/@href")
#         #每一页的所有职位的详情url
#         for link in links:
#             self.request_detail_page(link)
#             time.sleep(1)
#
#     def request_detail_page(self,url):
#         # self.driver.get(url)
#         self.driver.execute_script("window.open('%s')"%url)
#         self.driver.switch_to.window(self.driver.window_handles[1])
#
#         WebDriverWait(driver=self.driver,timeout=20).until(
#             EC.presence_of_element_located((By.XPATH,"//div[@class='job-name']/span[@class='name']"))
#         )
#         #获取职位详情页的源代码
#         source = self.driver.page_source
#         self.parse_detail_page(source)
#         #关闭当前详情页，并且切换到列表页
#         self.driver.close()
#         self.driver.switch_to.window(self.driver.window_handles[0])
#
#     def parse_detail_page(self,source):
#         html = etree.HTML(source)
#         position_name = html.xpath("//span[@class='name']/text()")[0]
#         job_request_spans = html.xpath("//dd[@class='job_request']//span")
#         salary = job_request_spans[0].xpath('.//text()')[0].strip()
#         city = job_request_spans[1].xpath('.//text()')[0].strip()
#         city = re.sub(r"[\s/]","",city)
#         work_years = job_request_spans[2].xpath('.//text()')[0].strip()
#         work_years = re.sub(r"[\s/]","",work_years)
#         education = job_request_spans[3].xpath('.//text()')[0].strip()
#         education = re.sub(r"[\s/]","",education)
#         desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
#         company_name = html.xpath("//h2[@class='fl']/text()")[0].strip()
#         position = {
#             'name':position_name,
#             'company_name':company_name,
#             'salary':salary,
#             'city': city,
#             'work_years': work_years,
#             'education': education,
#             'desc': desc,
#         }
#         self.position.append(position)
#         print(position)
#         print('-'*200)
#
# if __name__ == '__main__':
#     spider = LagouSpider()
#     spider.run()


#threading
# import requests
# from lxml import etree
# from urllib import request
# import os
# import re
# import threading
# from queue import Queue
#
# class Producer(threading.Thread):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
#         'Referer': 'https://movie.douban.com/'
#     }
#
#     def __init__(self, page_queue, img_queue, *args, **kwargs):
#         super(Producer, self).__init__(*args, **kwargs)
#         self.page_queue = page_queue
#         self.img_queue = img_queue
#
#     def run(self):
#         while True:
#             if self.page_queue.empty():
#                 break
#             url = self.page_queue.get()
#             self.parse_page(url)
#
#     def parse_page(self,url):
#         response = requests.get(url,headers=self.headers)
#         text = response.text
#         html = etree.HTML(text)
#         imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
#         for img in imgs:
#             # print(etree.tostring(img))
#             #图片地址
#             img_url = img.get('data-original')
#             #图片名字
#             alt = img.get('alt')
#             #替换掉名字里面的特殊字符
#             alt = re.sub(r'[\?？\.，。！!\*]','',alt)
#             #获取图片的后缀名（.gif .jpg）
#             suffix = os.path.splitext(img_url)[1]
#             #保存的时候完整的图片名字
#             filename = alt + suffix
#             self.img_queue.put((img_url,filename))
#
#
# class Consumer(threading.Thread):
#     def __init__(self,page_queue,img_queue,*args,**kwargs):
#         super(Consumer, self).__init__(*args,**kwargs)
#         self.page_queue = page_queue
#         self.img_queue = img_queue
#
#     def run(self):
#         while True:
#             if self.img_queue.empty() and self.page_queue.empty():
#                 break
#             img_url,filename = self.img_queue.get()
#             request.urlretrieve(img_url, 'C:/Users/Administrator/Desktop/images/' + filename)
#             print("已下载完一张图片")
#
#
# def main():
#     page_queue = Queue(1000)
#     img_queue = Queue(10000)
#
#     for x in range(1,1000):
#         url = 'http://www.doutula.com/photo/list/?page=%d'%x
#         page_queue.put(url)
#
#     for x in range(10):
#         t = Producer(page_queue,img_queue)
#         t.start()
#
#     for x in range(10):
#         t = Consumer(page_queue,img_queue)
#         t.start()
#
# if __name__ == '__main__':
#     main()






#下载远程数据
#request.urlretrieve(img_url,'C:/Users/Administrator/Desktop/images/'+filename)