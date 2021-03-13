from gevent import monkey
monkey.patch_all()
import requests,gevent,time,csv
from bs4 import BeautifulSoup
from gevent.queue import Queue
start = time.time()
url_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
for i in range(10):
    num = i+1
    url1 = 'http://www.boohee.com/food/view_menu?page='+str(num)
    url_list.append(url1)
    for x in range(10):
        number = x+1
        url2 = 'http://www.boohee.com/food/group/'+str(num)+'?page='+str(number)
        url_list.append(url2)
work = Queue()
for url in url_list:
    work.put_nowait(url)

def bohe():
    while not work.empty():
        url = work.get_nowait()
        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.text,'html.parser')
        foods = soup.find_all('li',class_='item clearfix')
        for i in foods:
            data = i.find('h4')
            data2 = i.find('p')
            data3 = i.find('a')
            name = data.text.strip()
            hot = data2.text.strip()
            food_url = 'http://www.boohee.com'+data3['href']
            writer.writerow([name,hot,food_url])
            print(name,hot,food_url)
csv_file = open('food_hot.csv','w',newline='',encoding='utf-8')
writer = csv.writer(csv_file)
tasks_list = []
for i in range(5):
    task = gevent.spawn(bohe)
    tasks_list.append(task)
gevent.joinall(tasks_list)
end = time.time()
print(end-start)