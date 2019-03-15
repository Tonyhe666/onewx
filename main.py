# !/usr/bin/python
# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler


class Main:
    def __init__(self):
        self.useragent = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.one_url = "http://wufazhuce.com"
        self.weather_url = "http://t.weather.sojson.com/api/weather/city/101010100"

    def getone(self):
        resp = requests.get(self.one_url,headers=self.useragent)
        soup_text = BeautifulSoup(resp.text, 'lxml')
        msg = soup_text.find_all('div',class_="fp-one-cita")[0].text
        #print(msg)
        return msg

    def getWeather(self):
        resp = requests.get(self.weather_url)
        strjson = resp.json()
        if strjson["status"] == 200 :
            #print(strjson["data"]["forecast"][0])
            today = strjson["data"]["forecast"][0]
            msg = "%s\n%s\n%s\n%s/%s\n%s:%s\npm2.5:%d\n%s\n" % (today['ymd'], today['week'], today['type'], today['high'], today['low'], today['fx'], today['fl'],strjson["data"]['pm25'], today['notice'])
            #print(msg)
            return msg
        pass

    def sendwx(self):
        #print("sendwx~")
        friends = itchat.search_friends(name='heliang')
        uuid = friends[0].get('UserName')
        one = self.getone()
        weather = self.getWeather()
        msg = weather + one
        itchat.send(msg, toUserName=uuid)

    def scheduler(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.sendwx, 'cron', hour=8, minute=30)
        #scheduler.add_job(self.sendwx, 'interval', seconds=120)
        scheduler.start()

    def run(self):
        itchat.auto_login(hotReload=True,enableCmdQR=2)
        self.scheduler()
        itchat.run()


if __name__ == '__main__':
    Main().run()