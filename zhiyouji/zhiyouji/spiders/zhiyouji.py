import scrapy
import bs4
from ..items import ZhiyoujiItem
class ZhiyoujiSpider(scrapy.Spider):
    name = 'zhiyouji'
    allowed_domains = ['www.jobui.com']
    start_urls = ['https://www.jobui.com/rank/company/']
    def parse(self,response):
        bs = bs4.BeautifulSoup(response.text,'html.parser')
        ul_list = bs.find_all('ul',class_='textList flsty cfix')
        for ul in ul_list:
            a_list = ul.find_all('a')
            for a in a_list:
                company_id = a['href']
                url = 'https://www.jobui.com{id}jobs'
                real_url = url.format(id = company_id)
                yield scrapy.Request(real_url,callback=self.parse_job)
    def parse_job(self,response):
        bs = bs4.BeautifulSoup(response.text,'html.parser')
        company = bs.find(id='companyH1').text
        datas = bs.find_all('div',class_='c-job-list')
        for data in datas:
            item = ZhiyoujiItem()
            item['company'] = company
            item['name'] = data.find('a').find('h3')['title']
            item['city'] = data.find_all('span')[0]['title']
            item['desc'] = data.find_all('span')[1]['title']
            print(item['company'],item['name'],item['city'],item['desc'])
            yield item
