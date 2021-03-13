import scrapy
from bs4 import BeautifulSoup
from ..items import DoubanItem
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['www.douban.com']
    start_urls = []
    for i in range(5):
        num = i*25
        url = 'https://book.douban.com/top250?start=' + str(num)
        start_urls.append(url)
    def parse(self,response):
        bs = BeautifulSoup(response.text,'html.parser')
        datas = bs.find_all('tr',class_='item')
        for data in datas:
            item = DoubanItem()
            item['title'] = data.find_all('a')[1]['title']
            item['publish'] = data.find('p',class_='pl').text
            item['score'] = data.find('span',class_='rating_nums').text
            print(item['title'])
            yield item


