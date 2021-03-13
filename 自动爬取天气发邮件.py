import smtplib,requests,time,schedule
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
user = input('请输入邮箱:')
pwd = input('请输入授权码:')
remail = input('请输入收件箱地址:')
def comment():
    url = 'http://www.weather.com.cn/weather/101240601.shtml'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    res = requests.get(url=url,header=header)
    soup = BeautifulSoup(res.text,'html.parser')
    data1 = soup.find('p',class_='wea')
    data2 = soup.find('p',class_='tem')
    wea = data1.text
    tem = data2.text
    return wea,tem
def mail(wea,tem):
    mailhost = 'smtp.qq.com'
    qqmail = smtplib.SMTP()
    #实例化一个smtplib模块里的SMTP类的对象，这样就可以SMTP对象的方法和属性了
    qqmail.connect(mailhost,25)
    qqmail.login(user,pwd)
    content = wea+'/n'+tem
    message = MIMEText(content,'plain','utf-8')
    #实例化一个MIMEText邮件对象，该对象需要写进三个参数，分别是邮件正文，文本格式和编码.
    subject = '天气预报'
    message['Subject'] = Header(subject,'utf-8')
    #在等号的右边，是实例化了一个Header邮件头对象，该对象需要写入两个参数，分别是邮件主题和编码，然后赋值给等号左边的变量message['Subject']。
    try:
        qqmail.sendmail(user,remail,message.as_string())
    #发送邮件，调用了sendmail()方法，写入三个参数，分别是发件人，收件人，和字符串格式的正文。
        print('发送成功')
    except:
        print('发送失败')
    qqmail.quit()
def job():
    print('任务开始!')
    wea,tem = comment()
    mail(wea,tem)
    print('任务完成!')
schedule.every().day.at('07:30').do(job)
while True:
    schedule.run_pending()
    time.sleep(1)